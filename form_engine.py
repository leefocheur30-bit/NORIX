# engines/form_engine.py
# Moteur de forme récente (5 derniers matchs)

import logging
from data.api_provider import get_fixtures
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class FormEngine:
    def __init__(self):
        self.name = "FormEngine"
        self.n_matches = 5  # Nombre de matchs récents à analyser

    def get_recent_form(self, team_id: int, league_id: int, current_date: str) -> dict:
        """
        Récupère les 5 derniers matchs d'une équipe et calcule :
        - points / matchs
        - buts marqués / match
        - buts encaissés / match
        - pourcentage de victoires
        """
        try:
            # Récupérer les matchs des 45 derniers jours
            end_date = datetime.strptime(current_date, "%Y-%m-%d")
            start_date = end_date - timedelta(days=45)
            
            fixtures = get_fixtures(
                league_id=league_id,
                season=end_date.year,
                date=start_date.strftime("%Y-%m-%d")
            )
            
            if not fixtures:
                return self._default_form()

            # Filtrer les matchs de l'équipe (home ou away)
            team_matches = []
            for f in fixtures:
                if f['teams']['home']['id'] == team_id or f['teams']['away']['id'] == team_id:
                    if f['fixture']['status']['short'] in ['FT', 'AET', 'PEN']:
                        team_matches.append(f)

            # Prendre les 5 derniers
            team_matches = team_matches[-self.n_matches:]
            
            if len(team_matches) < 3:
                return self._default_form()

            # Calculer les stats
            total_points = 0
            total_goals_for = 0
            total_goals_against = 0
            total_wins = 0
            total_matches = len(team_matches)

            for f in team_matches:
                home_id = f['teams']['home']['id']
                away_id = f['teams']['away']['id']
                home_goals = f['goals']['home']
                away_goals = f['goals']['away']

                if home_id == team_id:
                    # L'équipe joue à domicile
                    goals_for = home_goals
                    goals_against = away_goals
                    if home_goals > away_goals:
                        total_points += 3
                        total_wins += 1
                    elif home_goals == away_goals:
                        total_points += 1
                    else:
                        total_points += 0
                else:
                    # L'équipe joue à l'extérieur
                    goals_for = away_goals
                    goals_against = home_goals
                    if away_goals > home_goals:
                        total_points += 3
                        total_wins += 1
                    elif away_goals == home_goals:
                        total_points += 1
                    else:
                        total_points += 0

                total_goals_for += goals_for
                total_goals_against += goals_against

            return {
                "matches_played": total_matches,
                "points": total_points,
                "points_per_match": total_points / total_matches if total_matches > 0 else 1.0,
                "goals_for_avg": total_goals_for / total_matches if total_matches > 0 else 1.0,
                "goals_against_avg": total_goals_against / total_matches if total_matches > 0 else 1.0,
                "win_percentage": (total_wins / total_matches) if total_matches > 0 else 0.0,
                "form_score": (total_points / (total_matches * 3)) if total_matches > 0 else 0.5
            }

        except Exception as e:
            logger.error(f"Erreur lors du calcul de la forme : {e}")
            return self._default_form()

    def _default_form(self) -> dict:
        """Valeurs par défaut quand les données sont insuffisantes."""
        return {
            "matches_played": 5,
            "points": 6,
            "points_per_match": 1.2,
            "goals_for_avg": 1.2,
            "goals_against_avg": 1.1,
            "win_percentage": 0.4,
            "form_score": 0.5
        }