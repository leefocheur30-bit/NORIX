# data/api_provider.py
import requests
import config
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIFootballProvider:
    def __init__(self):
        self.base_url = config.SPORTS_API_URL
        self.api_key = config.SPORTS_API_KEY
        self.headers = {
            "x-apisports-key": self.api_key,
            "Accept": "application/json"
        }
        self.last_request_time = 0
        self.min_delay = 1.5
        logger.info("✅ API Football Provider initialisé")
    
    def _make_request(self, endpoint: str, params: dict = None, retries: int = 2):
        now = time.time()
        wait = self.min_delay - (now - self.last_request_time)
        if wait > 0:
            time.sleep(wait)
        
        url = f"{self.base_url}/{endpoint}"
        for attempt in range(retries + 1):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                self.last_request_time = time.time()
                if response.status_code == 429:
                    logger.warning("Trop de requêtes (429). Attente 5s...")
                    time.sleep(5)
                    continue
                response.raise_for_status()
                data = response.json()
                if data.get('errors') and data['errors']:
                    logger.error(f"Erreur API : {data['errors']}")
                    return None
                # On retourne la partie response, qui peut être une liste ou un dict
                return data.get('response')
            except requests.exceptions.RequestException as e:
                logger.error(f"Erreur réseau : {e}")
                if attempt < retries:
                    time.sleep(2)
                else:
                    return None
        return None

    def get_fixtures(self, date: str = None, league_id: int = None, season: int = None) -> list:
        params = {}
        if date:
            params['date'] = date
        if league_id:
            params['league'] = league_id
        if season:
            params['season'] = season
        result = self._make_request("fixtures", params)
        return result if isinstance(result, list) else []

    def get_fixture(self, fixture_id: int) -> dict:
        params = {'id': fixture_id}
        result = self._make_request("fixtures", params)
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return None

    def get_team_statistics(self, team_id: int, league_id: int, season: int) -> dict:
        """
        Récupère les statistiques d'une équipe.
        Si la saison demandée échoue, essaie 2024, 2023, 2022.
        """
        seasons_to_try = [season]
        if season > 2024:
            seasons_to_try = [season, 2024, 2023, 2022]
        elif season < 2022:
            seasons_to_try = [season, 2022, 2023, 2024]
        
        for s in seasons_to_try:
            params = {'team': team_id, 'league': league_id, 'season': s}
            result = self._make_request("teams/statistics", params)
            # result peut être une liste (rare) ou un dict
            if result is not None:
                # Si c'est une liste non vide, on prend le premier élément
                if isinstance(result, list) and len(result) > 0:
                    logger.info(f"Stats trouvées pour la saison {s}")
                    return result[0]
                # Si c'est un dictionnaire, on le retourne directement
                elif isinstance(result, dict):
                    logger.info(f"Stats trouvées pour la saison {s}")
                    return result
            # Sinon, on continue avec la saison suivante
        logger.warning(f"Impossible d'obtenir les stats pour la saison {season} (fallback échoué)")
        return None

    def get_teams(self, league_id: int, season: int) -> list:
        params = {'league': league_id, 'season': season}
        result = self._make_request("teams", params)
        return result if isinstance(result, list) else []

    def get_leagues(self) -> list:
        result = self._make_request("leagues")
        return result if isinstance(result, list) else []


# Singleton pour les fonctions standalone
_provider = None

def _get_provider():
    global _provider
    if _provider is None:
        _provider = APIFootballProvider()
    return _provider

def get_fixtures(date: str = None, league_id: int = None, season: int = None) -> list:
    return _get_provider().get_fixtures(date, league_id, season)

def get_fixture(fixture_id: int) -> dict:
    return _get_provider().get_fixture(fixture_id)

def get_team_statistics(team_id: int, league_id: int, season: int) -> dict:
    return _get_provider().get_team_statistics(team_id, league_id, season)