# engines/btts.py
import math

class BTTSEngine:
    def __init__(self):
        self.name = "BTTS"

    def calculate(self, home_lambda: float, away_lambda: float) -> dict:
        """
        Calcule la probabilité que les deux équipes marquent (BTTS Oui/Non).
        """
        def poisson(lam, k):
            if lam <= 0:
                return 1.0 if k == 0 else 0.0
            return (math.exp(-lam) * (lam ** k)) / math.factorial(k)

        # Probabilité que les deux marquent = 1 - (home 0 ou away 0)
        home_zero = poisson(home_lambda, 0)
        away_zero = poisson(away_lambda, 0)
        home_not_zero = 1 - home_zero
        away_not_zero = 1 - away_zero

        both_score = home_not_zero * away_not_zero
        return {
            "btts_yes": both_score,
            "btts_no": 1.0 - both_score
        }