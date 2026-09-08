# engines/weight_optimizer.py
# Optimisation automatique des poids des modèles en fonction des performances historiques

import sqlite3
import numpy as np
from scipy.optimize import minimize
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeightOptimizer:
    def __init__(self, db_path="noryx.db"):
        self.db_path = db_path
        self.weights = {"poisson": 0.40, "elo": 0.30, "monte_carlo": 0.30}
        self.bounds = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]

    def load_historical_data(self) -> tuple:
        """Charge les données historiques depuis la base."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                pred_home, pred_draw, pred_away,
                actual_result
            FROM predictions
            WHERE actual_result IS NOT NULL
        """)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            logger.warning("Aucune donnée historique disponible.")
            return [], []

        predictions = []
        actuals = []
        for row in rows:
            pred_home, pred_draw, pred_away, actual = row
            predictions.append({"home": pred_home, "draw": pred_draw, "away": pred_away})
            actuals.append(actual)

        return predictions, actuals

    def objective(self, weights: list) -> float:
        """
        Fonction objectif à minimiser.
        weights = [poisson_weight, elo_weight, monte_carlo_weight]
        """
        poisson_w, elo_w, mc_w = weights
        total = poisson_w + elo_w + mc_w
        if total == 0:
            return 1.0

        # Normaliser les poids
        poisson_w /= total
        elo_w /= total
        mc_w /= total

        # Charger les données (cache pour éviter de recharger à chaque itération)
        if not hasattr(self, '_predictions'):
            self._predictions, self._actuals = self.load_historical_data()
        
        if not self._predictions:
            return 1.0

        # Calculer la perte (Brier Score) avec ces poids
        total_loss = 0.0
        for pred, actual in zip(self._predictions, self._actuals):
            # Fusionner les prédictions
            fused = {
                "home": poisson_w * pred["home"] + elo_w * pred["home"] + mc_w * pred["home"],
                "draw": poisson_w * pred["draw"] + elo_w * pred["draw"] + mc_w * pred["draw"],
                "away": poisson_w * pred["away"] + elo_w * pred["away"] + mc_w * pred["away"]
            }
            # Normaliser
            total_prob = sum(fused.values())
            if total_prob > 0:
                for k in fused:
                    fused[k] /= total_prob
            
            # Brier Score pour ce match
            prob = fused.get(actual, 0.0)
            loss = (1 - prob) ** 2
            total_loss += loss

        return total_loss / len(self._predictions)

    def optimize(self) -> dict:
        """
        Lance l'optimisation des poids.
        Retourne les nouveaux poids optimisés.
        """
        logger.info("🔄 Optimisation des poids en cours...")
        
        # Charger les données
        self._predictions, self._actuals = self.load_historical_data()
        
        if not self._predictions:
            logger.warning("Pas assez de données pour l'optimisation.")
            return self.weights

        # Poids initiaux
        initial_weights = [self.weights["poisson"], self.weights["elo"], self.weights["monte_carlo"]]
        
        # Contraintes : poids >= 0
        bounds = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
        
        # Optimisation
        result = minimize(
            self.objective,
            initial_weights,
            method='L-BFGS-B',
            bounds=bounds,
            options={'maxiter': 100, 'disp': False}
        )

        if result.success:
            optimized = result.x
            # Normaliser
            total = sum(optimized)
            if total > 0:
                self.weights = {
                    "poisson": optimized[0] / total,
                    "elo": optimized[1] / total,
                    "monte_carlo": optimized[2] / total
                }
            else:
                self.weights = {"poisson": 0.33, "elo": 0.33, "monte_carlo": 0.34}
            
            logger.info(f"✅ Poids optimisés : {self.weights}")
            return self.weights
        else:
            logger.warning(f"⚠️ Optimisation échouée : {result.message}")
            return self.weights

    def apply_weights(self):
        """
        Applique les poids optimisés dans le fichier config.
        """
        # Sauvegarder dans un fichier
        import json
        with open("optimized_weights.json", "w") as f:
            json.dump(self.weights, f)
        logger.info(f"💾 Poids sauvegardés dans optimized_weights.json")

    def load_optimized_weights(self) -> dict:
        """Charge les poids optimisés depuis le fichier."""
        import json
        import os
        if os.path.exists("optimized_weights.json"):
            with open("optimized_weights.json", "r") as f:
                return json.load(f)
        return None


if __name__ == "__main__":
    # Test de l'optimisation
    optimizer = WeightOptimizer()
    weights = optimizer.optimize()
    optimizer.apply_weights()
    print(f"📊 Poids optimisés : {weights}")