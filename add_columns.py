# add_columns.py
import sqlite3

conn = sqlite3.connect("noryx.db")
cursor = conn.cursor()

for col in ['over_2_5', 'under_2_5', 'btts_yes', 'btts_no']:
    try:
        cursor.execute(f"ALTER TABLE predictions ADD COLUMN {col} REAL")
        print(f"✅ Colonne {col} ajoutée.")
    except sqlite3.OperationalError:
        print(f"ℹ️ Colonne {col} existe déjà.")

conn.commit()
conn.close()
print("✅ Terminé.")