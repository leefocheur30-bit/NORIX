from data.match import Match

from engines.poisson import (
    analyze_match as analyze_poisson,
    calculate_1x2,
)

from engines.elo import (
    analyze_match as analyze_elo,
)

from engines.consensus import (
    calculate_consensus,
    calculate_agreement,
)


match = Match(
    home_team="Team A",
    away_team="Team B",
    home_goals_avg=1.8,
    away_goals_avg=1.2,
    home_rank=3,
    away_rank=7,
    home_elo=1650,
    away_elo=1580,
)


poisson_results = analyze_poisson(match)

poisson_1x2 = calculate_1x2(
    poisson_results
)

elo_results = analyze_elo(match)

consensus = calculate_consensus(
    poisson_1x2,
    elo_results,
)

agreement = calculate_agreement(
    poisson_1x2,
    elo_results,
)


print()
print("==============================================")
print("        NORYX - CONSENSUS ENGINE")
print("==============================================")
print()

print(
    f"Match : {match.home_team} "
    f"vs {match.away_team}"
)

print()

print("POISSON")
print("----------------------------------------------")

print(
    f"Team A : "
    f"{poisson_1x2['home_win'] * 100:.2f}%"
)

print(
    f"Nul : "
    f"{poisson_1x2['draw'] * 100:.2f}%"
)

print(
    f"Team B : "
    f"{poisson_1x2['away_win'] * 100:.2f}%"
)

print()

print("ELO")
print("----------------------------------------------")

print(
    f"Team A : "
    f"{elo_results['home'] * 100:.2f}%"
)

print(
    f"Team B : "
    f"{elo_results['away'] * 100:.2f}%"
)

print()

print("CONSENSUS")
print("----------------------------------------------")

print(
    f"Team A : "
    f"{consensus['home'] * 100:.2f}%"
)

print(
    f"Nul : "
    f"{consensus['draw'] * 100:.2f}%"
)

print(
    f"Team B : "
    f"{consensus['away'] * 100:.2f}%"
)

print()

print("ACCORD DES MOTEURS")
print("----------------------------------------------")

if agreement["status"] == "AGREEMENT":
    print("✅ Les deux moteurs sont d'accord.")
else:
    print("⚠️ Les deux moteurs ne sont pas d'accord.")

print(
    f"Score d'accord : "
    f"{agreement['score'] * 100:.0f}%"
)

print()

print("==============================================")