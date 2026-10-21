"""Recharge les produits depuis produits_data.py (les demandes sont conservées)."""
import sqlite3

from app import DB_PATH, charger_produits

with sqlite3.connect(DB_PATH) as db:
    charger_produits(db)

print("Produits rechargés depuis produits_data.py.")
