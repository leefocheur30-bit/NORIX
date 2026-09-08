# performance_report.py
# Tableau de bord des performances NORYX

import sqlite3
import numpy as np
import logging
from datetime import datetime
from tabulate import tabulate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceReport:
    def __init__(self, db_path="noryx.db"):
        self.db_path = db_path

    def compute_metrics(self) -> dict:
        """Calcule toutes les métriques à partir des prédictions en base."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Récupérer toutes les prédictions avec résultat réel
        cursor.execute("""
            SELECT 
                pred_home, pred_draw, pred_away,
                prediction,
                actual_result,
                confidence,
                risk_level
            FROM predictions
            WHERE actual_result IS NOT NULL
        """)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {"error": "Aucun résultat réel disponible"}

        predictions = []
        actuals = []
        pred_labels = []
        confidences = []
        risk_levels = []

        for row in rows:
            pred_home, pred_draw, pred_away, pred_label, actual, conf, risk = row
            predictions.append({"home": pred_home, "draw": pred_draw, "away": pred_away})
            actuals.append(actual)
            pred_labels.append(pred_label)
            confidences.append(conf)
            risk_levels.append(risk)

        total = len(rows)

        # 1. Précision 1X2
        correct = sum(1 for p, a in zip(pred_labels, actuals) if p == a)
        accuracy = correct / total if total > 0 else 0.0

        # 2. Brier Score (plus petit = meilleur)
        brier = self._brier_score(predictions, actuals)

        # 3. Log Loss (plus petit = meilleur)
        logloss = self._log_loss(predictions, actuals)

        # 4. Erreur de calibration
        cal_error = self._calibration_error(predictions, actuals)

        # 5. Résultats par niveau de risque
        risk_performance = {}
        for level in ["FAIBLE", "MODÉRÉ", "ÉLEVÉ"]:
            indices = [i for i, r in enumerate(risk_levels) if r == level]
            if indices:
                correct_risk = sum(1 for i in indices if pred_labels[i] == actuals[i])
                risk_performance[level] = {
                    "total": len(indices),
                    "correct": correct_risk,
                    "accuracy": correct_risk / len(indices) if indices else 0.0
                }

        # 6. Simulation de paris (mise de 10€ sur chaque pronostic)
        profit = self._simulate_betting(pred_labels, actuals, confidences)

        return {
            "total_predictions": total,
            "accuracy": accuracy,
            "brier_score": brier,
            "log_loss": logloss,
            "calibration_error": cal_error,
            "risk_performance": risk_performance,
            "profit": profit,
            "correct_predictions": correct,
            "wrong_predictions": total - correct
        }

    def _brier_score(self, predictions, actuals):
        """Brier Score : moyenne des carrés des écarts."""
        scores = []
        for pred, actual in zip(predictions, actuals):
            prob = pred.get(actual, 0.0)
            scores.append((1 - prob) ** 2)
        return np.mean(scores)

    def _log_loss(self, predictions, actuals, eps=1e-15):
        """Log Loss : moyenne des logs négatifs des probabilités."""
        scores = []
        for pred, actual in zip(predictions, actuals):
            prob = max(eps, min(1 - eps, pred.get(actual, 0.0)))
            scores.append(-np.log(prob))
        return np.mean(scores)

    def _calibration_error(self, predictions, actuals, n_bins=10):
        """Erreur de calibration simplifiée."""
        probs = []
        for pred, actual in zip(predictions, actuals):
            prob = pred.get(actual, 0.0)
            probs.append(prob)
        return np.std(probs)

    def _simulate_betting(self, pred_labels, actuals, confidences, stake=10.0):
        """Simulation de paris : mise de 10€ sur chaque pronostic."""
        profit = 0.0
        for pred, actual, conf in zip(pred_labels, actuals, confidences):
            # On mise uniquement si la confiance est >= 60%
            if conf >= 0.60:
                if pred == actual:
                    # Gain : cote approximative = 1 / probabilité (on estime)
                    # On utilise une cote moyenne de 2.0 pour simplifier
                    odds = 2.0
                    profit += stake * (odds - 1)
                else:
                    profit -= stake
        return profit

    def display(self):
        """Affiche le tableau de bord dans la console."""
        metrics = self.compute_metrics()

        if "error" in metrics:
            print(f"\n❌ {metrics['error']}")
            return

        print("\n" + "="*70)
        print("   📊  TABLEAU DE BORD NORYX - PERFORMANCE  📊")
        print("="*70)

        # Métriques globales
        print(f"\n📈 Métriques globales ({metrics['total_predictions']} prédictions) :")
        print(f"   ✅ Précision 1X2 : {metrics['accuracy']*100:.2f}%")
        print(f"   📊 Brier Score   : {metrics['brier_score']:.4f} (idéal = 0)")
        print(f"   📉 Log Loss      : {metrics['log_loss']:.4f} (idéal = 0)")
        print(f"   🎯 Calibration   : {metrics['calibration_error']:.4f} (plus petit = meilleur)")
        print(f"   💰 Profit simulé : {metrics['profit']:.2f} €")

        # Performance par risque
        print(f"\n⚠️  Performance par niveau de risque :")
        risk_perf = metrics['risk_performance']
        for level in ["FAIBLE", "MODÉRÉ", "ÉLEVÉ"]:
            if level in risk_perf:
                data = risk_perf[level]
                print(f"   {level} : {data['total']} pronostics, {data['correct']} justes ({data['accuracy']*100:.2f}%)")

        # Résumé
        print("\n" + "-"*70)
        if metrics['accuracy'] >= 0.60:
            print("🔥 BONNE PERFORMANCE : précision > 60%")
        elif metrics['accuracy'] >= 0.50:
            print("📊 PERFORMANCE MOYENNE : précision entre 50% et 60%")
        else:
            print("⚠️ PERFORMANCE À AMÉLIORER : précision < 50%")

        print("="*70 + "\n")


if __name__ == "__main__":
    report = PerformanceReport()
    report.display()