# engines/poisson.py
# Moteur Poisson : calcule les probabilités 1X2 à partir des lambdas

import math
import numpy as np

class PoissonEngine:
    def __init__(self):
        self.name = "Poisson"
        self.max_goals = 10  # On calcule jusqu'à 10-10

    def poisson_probability(self, lam: float, goals: int) -> float:
        """Calcule P(X = goals) avec la loi de Poisson."""
        if lam <= 0:
            return 1.0 if goals == 0 else 0.0
        return (math.exp(-lam) * (lam ** goals)) / math.factorial(goals)

    def calculate_1x2(self, home_lambda: float, away_lambda: float) -> dict:
        """
        Calcule les probabilités 1 (home), X (draw), 2 (away).
        Retourne un dictionnaire { "home": float, "draw": float, "away": float }
        """
        home_win = 0.0
        draw = 0.0
        away_win = 0.0

        # On parcourt tous les scores possibles
        for h_goals in range(self.max_goals + 1):
            for a_goals in range(self.max_goals + 1):
                prob = self.poisson_probability(home_lambda, h_goals) * \
                       self.poisson_probability(away_lambda, a_goals)
                
                if h_goals > a_goals:
                    home_win += prob
                elif h_goals == a_goals:
                    draw += prob
                else:
                    away_win += prob

        # Normalisation au cas où (pour être sûr que la somme = 1)
        total = home_win + draw + away_win
        if total > 0:
            return {
                "home": home_win / total,
                "draw": draw / total,
                "away": away_win / total
            }
        else:
            return {"home": 0.33, "draw": 0.33, "away": 0.33}