# engines/lambda_engine.py
import logging
from engines.form_engine import FormEngine

logger = logging.getLogger(__name__)

class LambdaEngine:
    def __init__(self, home_advantage=1.10, min_lambda=0.15, max_lambda=5.0):
        self.home_advantage = home_advantage
        self.min_lambda = min_lambda
        self.max_lambda = max_lambda
        self.form_engine = FormEngine()
        self.form_weight = 0.30  # Poids de la forme dans l'ajustement

    def calculate(self, match, current_date: str = None) -> dict:
        """
        Calcule les lambdas (moyennes de buts) en tenant compte de la forme récente.
        """
        import datetime

        # 1. Récupérer les moyennes de base
        home_goals_avg = float(getattr(match, 'home_goals_avg', 1.2))
        away_goals_avg = float(getattr(match, 'away_goals_avg', 1.1))

        # 2. Récupérer la forme récente si disponible
        current_date = current_date or datetime.datetime.now().strftime("%Y-%m-%d")
        
        home_form = self.form_engine.get_recent_form(
            match.home_id, match.league_id, current_date
        )
        away_form = self.form_engine.get_recent_form(
            match.away_id, match.league_id, current_date
        )

        # 3. Ajuster les lambdas avec la forme
        home_form_factor = 1.0 + (home_form['form_score'] - 0.5) * self.form_weight
        away_form_factor = 1.0 + (away_form['form_score'] - 0.5) * self.form_weight

        home_lambda = home_goals_avg * self.home_advantage * home_form_factor
        away_lambda = away_goals_avg * away_form_factor

        # 4. Limiter les valeurs
        home_lambda = max(self.min_lambda, min(self.max_lambda, home_lambda))
        away_lambda = max(self.min_lambda, min(self.max_lambda, away_lambda))

        logger.info(f"📊 Lambda avec forme : home={home_lambda:.2f} (facteur {home_form_factor:.2f}), "
                   f"away={away_lambda:.2f} (facteur {away_form_factor:.2f})")

        return {
            "home": home_lambda,
            "away": away_lambda,
            "total": home_lambda + away_lambda
        }