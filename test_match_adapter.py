from datetime import datetime

from data.api_provider import ApiFootballProvider
from data.match_adapter import MatchAdapter


print()
print("==============================================")
print("       NORYX - MATCH ADAPTER TEST")
print("==============================================")
print()


try:

    provider = ApiFootballProvider()

    today = datetime.now().strftime("%Y-%m-%d")

    print(
        f"Recherche des matchs du {today}..."
    )

    print()

    fixtures = provider.get_fixtures(today)

    print(
        f"Matchs récupérés : {len(fixtures)}"
    )

    print()

    if not fixtures:

        print(
            "Aucun match disponible pour cette date."
        )

    else:

        fixture = fixtures[0]

        match = MatchAdapter.from_api_fixture(
            fixture
        )

        print("MATCH NORYX")
        print("----------------------------------------------")

        print(
            f"Domicile : {match.home_team}"
        )

        print(
            f"Extérieur : {match.away_team}"
        )

        print(
            f"ELO domicile : {match.home_elo}"
        )

        print(
            f"ELO extérieur : {match.away_elo}"
        )

        print()

        print("✅ CONVERSION API → MATCH RÉUSSIE")

except Exception as error:

    print()
    print("❌ ERREUR")
    print("----------------------------------------------")
    print(error)

print()
print("==============================================")