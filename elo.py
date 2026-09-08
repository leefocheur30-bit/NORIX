# engines/elo.py
# Moteur ELO : calcule les forces relatives et estime le nul

import config

class EloEngine:
    def __init__(self):
        self.name = "ELO"
        self.home_advantage = config.HOME_ADVANTAGE  # valeur du fichier config.py

    def to_1x2(self, home_elo: float, away_elo: float) -> dict:
        """
        Convertit les ELO en probabilités 1X2.
        """
        # Probabilité de victoire "pure" (sans nul)
        home_win_raw = 1.0 / (1.0 + 10 ** ((away_elo - (home_elo + self.home_advantage)) / 400.0))
        away_win_raw = 1.0 / (1.0 + 10 ** (((home_elo + self.home_advantage) - away_elo) / 400.0))

        # Calcul du nul : plus les équipes sont proches, plus le nul est élevé
        diff = abs(home_elo - away_elo)
        # Si diff = 0, draw = 0.40 ; si diff = 400, draw = 0.10
        draw_prob = 0.40 - (0.30 * min(diff / 400.0, 1.0))
        draw_prob = max(0.10, draw_prob)

        # On ajuste les victoires pour que le total fasse 1
        factor = 1.0 - draw_prob
        home_win = home_win_raw * factor
        away_win = away_win_raw * factor

        return {
            "home": home_win,
            "draw": draw_prob,
            "away": away_win
        }