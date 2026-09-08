# engines/monte_carlo.py
import numpy as np
import config

class MonteCarloEngine:
    def __init__(self, simulations=10000):
        self.simulations = getattr(config, 'MONTE_CARLO_SIMULATIONS', simulations)
        self.name = "Monte Carlo"

    def simulate(self, home_lambda: float, away_lambda: float) -> dict:
        """
        Simule le match un grand nombre de fois et retourne les probabilités 1X2.
        """
        home_goals = np.random.poisson(home_lambda, self.simulations)
        away_goals = np.random.poisson(away_lambda, self.simulations)

        home_wins = np.sum(home_goals > away_goals)
        draws = np.sum(home_goals == away_goals)
        away_wins = np.sum(home_goals < away_goals)

        total = self.simulations
        return {
            "home": home_wins / total,
            "draw": draws / total,
            "away": away_wins / total
        }