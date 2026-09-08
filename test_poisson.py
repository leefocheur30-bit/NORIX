from data.match import Match

from engines.poisson import (
    analyze_match,
    find_best_score,
    calculate_1x2,
    calculate_distribution_coverage,
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


results = analyze_match(match)

best_score = find_best_score(results)

probabilities_1x2 = calculate_1x2(results)

coverage = calculate_distribution_coverage(
    results
)


print()
print("==============================================")
print("       TEST NORYX - POISSON ENGINE")
print("==============================================")
print()

print(
    f"Match : {match.home_team} "
    f"vs {match.away_team}"
)

print()

print(
    f"Meilleur score : "
    f"{best_score['score']}"
)

print(
    f"Probabilité : "
    f"{best_score['probability'] * 100:.2f}%"
)

print()

print("PROBABILITÉS 1X2")
print("----------------------------------------------")

print(
    f"Victoire {match.home_team} : "
    f"{probabilities_1x2['home_win'] * 100:.2f}%"
)

print(
    f"Nul : "
    f"{probabilities_1x2['draw'] * 100:.2f}%"
)

print(
    f"Victoire {match.away_team} : "
    f"{probabilities_1x2['away_win'] * 100:.2f}%"
)

print()

print("COUVERTURE")
print("----------------------------------------------")

print(
    f"Capturée : "
    f"{coverage['total'] * 100:.4f}%"
)

print(
    f"Ignorée : "
    f"{coverage['ignored'] * 100:.4f}%"
)

print()
print("✅ TEST POISSON TERMINÉ")
print()
print("==============================================")