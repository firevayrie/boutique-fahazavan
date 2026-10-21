import re
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, g, jsonify, redirect, render_template, request, url_for

from produits_data import CONTACTS, PRODUITS

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "boutique.db"
SCHEMA_VERSION = 2

app = Flask(__name__)


# ---------- Base de données ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def charger_produits(db):
    """Remplace tous les produits par ceux de produits_data.py."""
    db.execute("DELETE FROM produits")
    db.execute("DELETE FROM sqlite_sequence WHERE name = 'produits'")
    db.executemany(
        "INSERT INTO produits (nom, description, prix, stock, categorie, image) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        PRODUITS,
    )


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        version = db.execute("PRAGMA user_version").fetchone()[0]
        if version < SCHEMA_VERSION:
            # ancienne structure (produits d'exemple) : on la remplace,
            # la table des demandes n'est pas touchée
            db.execute("DROP TABLE IF EXISTS produits")
        db.execute(
            """CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                description TEXT,
                prix INTEGER NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                categorie TEXT,
                image TEXT
            )"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS demandes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                email TEXT NOT NULL,
                type_site TEXT,
                message TEXT,
                date TEXT NOT NULL
            )"""
        )
        if version < SCHEMA_VERSION or db.execute("SELECT COUNT(*) FROM produits").fetchone()[0] == 0:
            charger_produits(db)
        db.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")


def chercher_produits(seulement_disponibles=True, q="", categorie=""):
    sql = "SELECT * FROM produits WHERE 1=1"
    params = []
    if seulement_disponibles:
        sql += " AND stock > 0"
    if q:
        sql += " AND (nom LIKE ? OR description LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    if categorie:
        sql += " AND categorie = ?"
        params.append(categorie)
    sql += " ORDER BY id"
    return get_db().execute(sql, params).fetchall()


def categories():
    rows = get_db().execute(
        "SELECT categorie FROM produits WHERE categorie IS NOT NULL "
        "GROUP BY categorie ORDER BY MIN(id)"
    ).fetchall()
    return [r["categorie"] for r in rows]


@app.template_filter("ariary")
def ariary(valeur):
    return f"{valeur:,}".replace(",", " ") + " Ar"


@app.context_processor
def donnees_communes():
    return {"contacts": CONTACTS}


# ---------- Pages ----------
@app.get("/")
def accueil():
    disponibles = chercher_produits(True)
    return render_template(
        "accueil.html",
        produits=disponibles[:6],
        tarifs=disponibles,
        merci=request.args.get("merci"),
        erreur=request.args.get("erreur"),
    )


@app.post("/contact")
def envoyer_demande():
    nom = request.form.get("nom", "").strip()
    email = request.form.get("email", "").strip()
    type_site = request.form.get("type_site", "").strip()
    message = request.form.get("message", "").strip()

    if not nom or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return redirect(
            url_for("accueil", erreur="Merci d'indiquer votre nom et un e-mail valide.", _anchor="contact")
        )

    db = get_db()
    db.execute(
        "INSERT INTO demandes (nom, email, type_site, message, date) VALUES (?, ?, ?, ?, ?)",
        (nom[:100], email[:150], type_site[:100], message[:2000], datetime.now().isoformat(timespec="seconds")),
    )
    db.commit()
    return redirect(url_for("accueil", merci=1, _anchor="contact"))


@app.get("/boutique")
def liste_produits():
    q = request.args.get("q", "").strip()
    cat = request.args.get("categorie", "").strip()
    return render_template(
        "produits.html",
        produits=chercher_produits(True, q, cat),
        categories=categories(),
        q=q,
        categorie=cat,
    )


@app.get("/produit/<int:produit_id>")
def page_produit(produit_id):
    produit = get_db().execute(
        "SELECT * FROM produits WHERE id = ?", (produit_id,)
    ).fetchone()
    if produit is None:
        abort(404)
    return render_template("produit.html", produit=produit)


@app.errorhandler(404)
def introuvable(_e):
    if request.path.startswith("/api/"):
        return jsonify(erreur="Produit introuvable"), 404
    return render_template("404.html"), 404


# ---------- API JSON ----------
def produit_en_dict(ligne):
    produit = dict(ligne)
    produit["disponible"] = produit["stock"] > 0
    produit["image_url"] = url_for("static", filename="produits/" + produit["image"]) if produit["image"] else None
    return produit


@app.get("/api/produits")
def api_liste():
    # ?disponible=0 pour inclure les produits en rupture
    seulement = request.args.get("disponible", "1") != "0"
    lignes = chercher_produits(
        seulement,
        request.args.get("q", "").strip(),
        request.args.get("categorie", "").strip(),
    )
    return jsonify([produit_en_dict(r) for r in lignes])


@app.get("/api/produits/<int:produit_id>")
def api_produit(produit_id):
    ligne = get_db().execute(
        "SELECT * FROM produits WHERE id = ?", (produit_id,)
    ).fetchone()
    if ligne is None:
        abort(404)
    return jsonify(produit_en_dict(ligne))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
