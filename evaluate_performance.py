# evaluate_performance.py
import sqlite3
import numpy as np
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def brier_score(predictions, actuals):
    """Calcule le Brier score (plus petit = meilleur)."""
    # predictions : liste de dict {home, draw, away}
    # actuals : liste de 'home', 'draw', 'away'
    scores = []
    for pred, actual in zip(predictions, actuals):
        prob = pred.get(actual, 0.0)
        scores.append((1 - prob) ** 2)
    return np.mean(scores)

def log_loss(predictions, actuals, eps=1e-15):
    """Calcule la Log Loss (plus petit = meilleur)."""
    scores = []
    for pred, actual in zip(predictions, actuals):
        prob = max(eps, min(1 - eps, pred.get(actual, 0.0)))
        scores.append(-np.log(prob))
    return np.mean(scores)

def calibration_error(predictions, actuals, n_bins=10):
    """Calcule l'erreur de calibration (plus petit = meilleur)."""
    # Simplifié : on classe les prédictions par probabilité du résultat prédit
    probs = []
    for pred, actual in zip(predictions, actuals):
        # Probabilité du résultat qui s'est produit
        prob = pred.get(actual, 0.0)
        probs.append(prob)
    # On pourrait faire plus sophistiqué, mais ici on retourne l'écart moyen
    return np.std(probs)

def compute_metrics():
    conn = sqlite3.connect("noryx.db")
    cursor = conn.cursor()

    # Récupérer les données
    cursor.execute("""
        SELECT pred_home, pred_draw, pred_away, actual_result
        FROM predictions
        WHERE actual_result IS NOT NULL
    """)
    rows = cursor.fetchall()

    if not rows:
        logger.warning("Aucun résultat réel disponible pour évaluation.")
        return

    predictions = [{"home": r[0], "draw": r[1], "away": r[2]} for r in rows]
    actuals = [r[3] for r in rows]

    # Précision 1X2
    correct = 0
    for pred, actual in zip(predictions, actuals):
        pred_label = max(pred, key=pred.get)
        if pred_label == actual:
            correct += 1
    accuracy = correct / len(rows)

    # Brier score
    brier = brier_score(predictions, actuals)

    # Log Loss
    logloss = log_loss(predictions, actuals)

    # Calibration
    cal_error = calibration_error(predictions, actuals)

    # Sauvegarder les métriques
    cursor.execute("""
        INSERT INTO performance_metrics (
            metric_date, total_predictions,
            accuracy_1x2, brier_score, log_loss, calibration_error
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d"),
        len(rows),
        accuracy,
        brier,
        logloss,
        cal_error
    ))

    conn.commit()
    conn.close()

    logger.info(f"📊 Métriques calculées : Précision={accuracy:.2%}, Brier={brier:.4f}, LogLoss={logloss:.4f}")

if __name__ == "__main__":
    compute_metrics()