"""Affiche les demandes reçues via les formulaires du site."""
import sqlite3

with sqlite3.connect("boutique.db") as db:
    lignes = db.execute(
        "SELECT id, date, nom, email, type_site, message FROM demandes ORDER BY id DESC"
    ).fetchall()

if not lignes:
    print("Aucune demande pour le moment.")
for id_, date, nom, email, type_site, message in lignes:
    print(f"#{id_} | {date} | {nom} | {email} | {type_site}")
    if message:
        print(f"    {message}")
