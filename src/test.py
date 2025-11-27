from utils.db_helper import setup_mongodb  # falls dein Modul so heißt
from pymongo import MongoClient

db, db_name, coll_dict = setup_mongodb()
col = coll_dict["products"]

# Gruppieren nach einem gemeinsamen Feld (z.B. Name, SKU, filename, falls vorhanden)
from collections import defaultdict

grouped = defaultdict(list)

for doc in col.find():
    # Angenommen, filename enthält die Produkt-ID
    pid = doc.get("productid")  # oder parse aus 'path'
    grouped[pid].append(doc)

# Prüfen, welche IDs mehr als 1 Dokument haben
for pid, docs in grouped.items():
    if len(docs) > 1:
        print(f"{pid} → {len(docs)} documents")