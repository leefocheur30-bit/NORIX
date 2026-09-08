from data.provider import FakeDataProvider


provider = FakeDataProvider()


matches = provider.get_matches()


print()
print("==============================================")
print("        NORYX - DATA PROVIDER TEST")
print("==============================================")
print()

print(
    f"Nombre de matchs trouvés : "
    f"{len(matches)}"
)

print()

for match_info in matches:

    print(
        f"Match {match_info['id']} : "
        f"{match_info['home_team']} "
        f"vs "
        f"{match_info['away_team']}"
    )


match = provider.get_match_data(1)


print()
print("OBJET MATCH")
print("----------------------------------------------")

print(
    f"{match.home_team} "
    f"vs "
    f"{match.away_team}"
)

print(
    f"Moyenne buts domicile : "
    f"{match.home_goals_avg}"
)

print(
    f"Moyenne buts extérieur : "
    f"{match.away_goals_avg}"
)

print(
    f"ELO domicile : "
    f"{match.home_elo}"
)

print(
    f"ELO extérieur : "
    f"{match.away_elo}"
)

print()
print("✅ DATA PROVIDER RETOURNE UN OBJET MATCH")
print()
print("==============================================")