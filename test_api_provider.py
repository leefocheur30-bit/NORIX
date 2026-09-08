from datetime import datetime

from data.api_provider import (
    ApiFootballProvider,
)


print()
print("==============================================")
print("       NORYX - API FOOTBALL TEST")
print("==============================================")
print()


try:

    provider = ApiFootballProvider()

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    print(
        f"Recherche des matchs du {today}..."
    )

    print()

    fixtures = provider.get_fixtures(
        today
    )

    print(
        f"Matchs récupérés : {len(fixtures)}"
    )

    print()

    if fixtures:

        print("PREMIERS MATCHS")
        print("----------------------------------------------")

        for fixture in fixtures[:5]:

            data = (
                provider.fixture_to_basic_data(
                    fixture
                )
            )

            print(
                f"{data['id']} : "
                f"{data['home_team']} "
                f"vs "
                f"{data['away_team']}"
            )

    else:

        print(
            "Aucun match trouvé pour cette date."
        )

    print()
    print("✅ CONNEXION API RÉUSSIE")

except Exception as error:

    print()
    print("❌ ERREUR API")
    print("----------------------------------------------")
    print(error)

print()
print("==============================================")