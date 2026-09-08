class TeamStatistics:

    def __init__(
        self,
        team_id,
        league_id,
        season,
        matches_played=0,
        wins=0,
        draws=0,
        losses=0,
        goals_for_avg=0.0,
        goals_against_avg=0.0,
    ):
        self.team_id = team_id
        self.league_id = league_id
        self.season = season

        self.matches_played = matches_played

        self.wins = wins
        self.draws = draws
        self.losses = losses

        self.goals_for_avg = goals_for_avg
        self.goals_against_avg = goals_against_avg

    def __repr__(self):

        return (
            f"TeamStatistics("
            f"team_id={self.team_id}, "
            f"matches={self.matches_played}, "
            f"wins={self.wins}, "
            f"draws={self.draws}, "
            f"losses={self.losses}, "
            f"goals_for_avg={self.goals_for_avg}, "
            f"goals_against_avg={self.goals_against_avg}"
            f")"
        )


def parse_team_statistics(
    data,
    team_id,
    league_id,
    season,
):
    """
    Transforme la réponse API-Football
    en objet TeamStatistics.
    """

    if not data:
        raise ValueError(
            "Aucune statistique disponible."
        )

    fixtures = data.get(
        "fixtures",
        {}
    )

    played = fixtures.get(
        "played",
        {}
    )

    wins = fixtures.get(
        "wins",
        {}
    )

    draws = fixtures.get(
        "draws",
        {}
    )

    loses = fixtures.get(
        "loses",
        {}
    )

    goals = data.get(
        "goals",
        {}
    )

    goals_for = goals.get(
        "for",
        {}
    )

    goals_against = goals.get(
        "against",
        {}
    )

    goals_for_avg = goals_for.get(
        "average",
        {}
    )

    goals_against_avg = goals_against.get(
        "average",
        {}
    )

    return TeamStatistics(

        team_id=team_id,

        league_id=league_id,

        season=season,

        matches_played=played.get(
            "total",
            0
        ) or 0,

        wins=wins.get(
            "total",
            0
        ) or 0,

        draws=draws.get(
            "total",
            0
        ) or 0,

        losses=loses.get(
            "total",
            0
        ) or 0,

        goals_for_avg=float(
            goals_for_avg.get(
                "total",
                0
            ) or 0
        ),

        goals_against_avg=float(
            goals_against_avg.get(
                "total",
                0
            ) or 0
        ),
    )