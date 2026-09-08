from abc import ABC, abstractmethod

from data.match import Match


class DataProvider(ABC):
    """
    Contrat que toute source de données sportives
    de NORYX devra respecter.
    """

    @abstractmethod
    def get_matches(self):
        """
        Retourne les matchs disponibles.
        """
        raise NotImplementedError

    @abstractmethod
    def get_match_data(self, match_id):
        """
        Retourne un objet Match complet.
        """
        raise NotImplementedError


class FakeDataProvider(DataProvider):
    """
    Source fictive utilisée pendant le développement.
    """

    def get_matches(self):
        return [
            {
                "id": 1,
                "home_team": "Team A",
                "away_team": "Team B",
            }
        ]

    def get_match_data(self, match_id):

        if match_id != 1:
            raise ValueError(
                f"Match inconnu : {match_id}"
            )

        return Match(
            home_team="Team A",
            away_team="Team B",
            home_goals_avg=1.8,
            away_goals_avg=1.2,
            home_rank=3,
            away_rank=7,
            home_elo=1650,
            away_elo=1580,
        )