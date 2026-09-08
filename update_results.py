# update_results.py
# Met à jour les résultats réels des matchs passés

import sqlite3
import logging
from data.api_provider import get_fixture

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_results():
    """Met à jour les résultats réels pour les matchs terminés."""
    conn = sqlite3.connect("noryx.db")
    cursor = conn.cursor()

    # Récupérer les prédictions sans résultat
    cursor.execute("""
        SELECT id, fixture_id FROM predictions
        WHERE actual_result IS NULL
    """)
    rows = cursor.fetchall()

    if not rows:
        logger.info("Aucun match à mettre à jour.")
        conn.close()
        return

    for pred_id, fixture_id in rows:
        fixture_data = get_fixture(fixture_id)
        if not fixture_data:
            logger.warning(f"Fixture {fixture_id} introuvable.")
            continue

        # Vérifier si le match est terminé
        status = fixture_data['fixture']['status']['short']
        if status in ['FT', 'AET', 'PEN']:
            home_goals = fixture_data['goals']['home']
            away_goals = fixture_data['goals']['away']
            
            if home_goals > away_goals:
                result = 'home'
            elif home_goals < away_goals:
                result = 'away'
            else:
                result = 'draw'

            # Mettre à jour la base
            cursor.execute("""
                UPDATE predictions
                SET actual_result = ?
                WHERE id = ?
            """, (result, pred_id))
            conn.commit()
            logger.info(f"✅ Match {fixture_id} mis à jour : {result}")

    conn.close()

if __name__ == "__main__":
    update_results()
    print("✅ Mise à jour terminée. Lance 'python performance_report.py' pour voir les résultats.")