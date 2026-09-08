from data.api_provider import ApiFootballProvider
from data.team_statistics import parse_team_statistics


def main():

    provider = ApiFootballProvider()

    # Test avec une saison accessible au forfait Free
    team_id = 124
    league_id = 71
    season = 2024

    print("=" * 50)
    print("       TEST NORYX - TEAM STATISTICS")
    print("=" * 50)

    print()
    print(f"Équipe ID : {team_id}")
    print(f"Ligue ID  : {league_id}")
    print(f"Saison    : {season}")
    print()

    try:

        raw_statistics = provider.get_team_statistics(
            team_id=team_id,
            league_id=league_id,
            season=season,
        )

        statistics = parse_team_statistics(
            data=raw_statistics,
            team_id=team_id,
            league_id=league_id,
            season=season,
        )

        print("STATISTIQUES")
        print("-" * 50)

        print(
            f"Matchs joués        : "
            f"{statistics.matches_played}"
        )

        print(
            f"Victoires           : "
            f"{statistics.wins}"
        )

        print(
            f"Nuls                : "
            f"{statistics.draws}"
        )

        print(
            f"Défaites            : "
            f"{statistics.losses}"
        )

        print(
            f"Moy. buts marqués   : "
            f"{statistics.goals_for_avg:.2f}"
        )

        print(
            f"Moy. buts encaissés : "
            f"{statistics.goals_against_avg:.2f}"
        )

        print()
        print("=" * 50)
        print("TEST RÉUSSI")
        print("=" * 50)

    except Exception as error:

        print()
        print("ERREUR")
        print("-" * 50)
        print(error)

        print()
        print("=" * 50)
        print("TEST ÉCHOUÉ")
        print("=" * 50)


if __name__ == "__main__":
    main()