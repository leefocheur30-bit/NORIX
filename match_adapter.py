# data/match_adapter.py
import logging
from data.match import Match

logger = logging.getLogger(__name__)

class MatchAdapter:
    def to_match(self, fixture_data: dict, home_stats: dict, away_stats: dict) -> Match:
        """
        Convertit les données API en objet Match.
        Tous les champs sont convertis en nombres flottants si nécessaire.
        """
        # Extraire les infos de base
        home_team = fixture_data['teams']['home']['name']
        away_team = fixture_data['teams']['away']['name']
        league = fixture_data['league']['name']
        date = fixture_data['fixture']['date']

        # Fonction interne : extrait une valeur et la convertit en float
        def extract_float(stats, key, default=1.0):
            if stats is None or not isinstance(stats, dict):
                return float(default)
            if key == 'goals_for_avg':
                value = stats.get('goals', {}).get('for', {}).get('average', {}).get('total', default)
            elif key == 'goals_against_avg':
                value = stats.get('goals', {}).get('against', {}).get('average', {}).get('total', default)
            elif key == 'matches_played':
                value = stats.get('fixtures', {}).get('played', {}).get('total', default)
            elif key == 'wins':
                value = stats.get('fixtures', {}).get('wins', {}).get('total', default)
            elif key == 'draws':
                value = stats.get('fixtures', {}).get('draws', {}).get('total', default)
            elif key == 'losses':
                value = stats.get('fixtures', {}).get('losses', {}).get('total', default)
            else:
                value = stats.get(key, default)
            try:
                return float(value) if value != "" and value is not None else float(default)
            except (ValueError, TypeError):
                return float(default)

        # Extraire les statistiques avec conversion
        home_goals_avg = extract_float(home_stats, 'goals_for_avg', 1.2)
        away_goals_avg = extract_float(away_stats, 'goals_against_avg', 1.1)

        # Créer l'objet Match
        match = Match(
            home_team=home_team,
            away_team=away_team,
            home_elo=1500.0,
            away_elo=1500.0,
            home_goals_avg=home_goals_avg,
            away_goals_avg=away_goals_avg,
            home_rank=10,
            away_rank=10
        )

        # Ajouter des attributs supplémentaires (dont les ID pour la forme)
        match.league = league
        match.date = date
        match.home_id = fixture_data['teams']['home']['id']
        match.away_id = fixture_data['teams']['away']['id']
        match.league_id = fixture_data['league']['id']
        match.season = fixture_data['league']['season']

        logger.info(f"✅ Match adapté : {home_team} (ID {match.home_id}) vs {away_team} (ID {match.away_id})")
        return match