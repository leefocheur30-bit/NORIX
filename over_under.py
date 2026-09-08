# engines/over_under.py
import math

class OverUnderEngine:
    def __init__(self):
        self.name = "Over/Under"

    def calculate(self, home_lambda: float, away_lambda: float) -> dict:
        """
        Calcule les probabilités pour Over/Under 0.5, 1.5, 2.5, 3.5
        Retourne un dict avec les clés 'over_0.5', 'under_0.5', etc.
        """
        def poisson(lam, k):
            if lam <= 0:
                return 1.0 if k == 0 else 0.0
            return (math.exp(-lam) * (lam ** k)) / math.factorial(k)

        result = {}
        total_lambda = home_lambda + away_lambda

        # Distribution du total des buts (somme de deux Poissons indépendants)
        # On calcule jusqu'à 10 buts
        max_goals = 10
        probs = {}
        for h in range(max_goals + 1):
            for a in range(max_goals + 1):
                total = h + a
                prob = poisson(home_lambda, h) * poisson(away_lambda, a)
                probs[total] = probs.get(total, 0.0) + prob

        # Calcul Over/Under pour chaque seuil
        thresholds = [0.5, 1.5, 2.5, 3.5]
        for t in thresholds:
            over = sum(prob for goals, prob in probs.items() if goals > t)
            under = 1.0 - over
            result[f"over_{t}"] = over
            result[f"under_{t}"] = under

        return result