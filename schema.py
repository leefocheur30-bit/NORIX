# database/schema.py
import sqlite3
import logging

logger = logging.getLogger(__name__)

def init_database(db_path="noryx.db"):
    """Crée les tables si elles n'existent pas."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Table des analyses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fixture_id INTEGER UNIQUE,
            match_date TEXT,
            home_team TEXT,
            away_team TEXT,
            league TEXT,
            home_lambda REAL,
            away_lambda REAL,
            pred_home REAL,
            pred_draw REAL,
            pred_away REAL,
            prediction TEXT,  -- 'home', 'draw', 'away'
            confidence REAL,
            risk_level TEXT,
            signal TEXT,
            actual_result TEXT,  -- 'home', 'draw', 'away' (rempli après le match)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table des métriques de performance (calculées périodiquement)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_date TEXT,
            total_predictions INTEGER,
            accuracy_1x2 REAL,
            brier_score REAL,
            log_loss REAL,
            calibration_error REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    logger.info("✅ Base de données initialisée avec les tables.")

if __name__ == "__main__":
    init_database()