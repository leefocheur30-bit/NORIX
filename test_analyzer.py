from data.match import Match

from analysis.analyzer import analyze


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


result = analyze(match)


print()
print("================================================")
print("           NORYX - ANALYZER")
print("================================================")
print()

print(
    f"Match : {result.match.home_team} "
    f"vs {result.match.away_team}"
)

print()

print("POISSON")
print("-----------------------------------------------")

print(
    f"Team A : "
    f"{result.poisson['home_win'] * 100:.2f}%"
)

print(
    f"Nul : "
    f"{result.poisson['draw'] * 100:.2f}%"
)

print(
    f"Team B : "
    f"{result.poisson['away_win'] * 100:.2f}%"
)

print()

print("ELO")
print("-----------------------------------------------")

print(
    f"Team A : "
    f"{result.elo['home'] * 100:.2f}%"
)

print(
    f"Team B : "
    f"{result.elo['away'] * 100:.2f}%"
)

print()

print("MONTE CARLO")
print("-----------------------------------------------")

print(
    f"Team A : "
    f"{result.monte_carlo['home_win'] * 100:.2f}%"
)

print(
    f"Nul : "
    f"{result.monte_carlo['draw'] * 100:.2f}%"
)

print(
    f"Team B : "
    f"{result.monte_carlo['away_win'] * 100:.2f}%"
)

print()

print("CONSENSUS")
print("-----------------------------------------------")

print(
    f"Team A : "
    f"{result.consensus['home'] * 100:.2f}%"
)

print(
    f"Nul : "
    f"{result.consensus['draw'] * 100:.2f}%"
)

print(
    f"Team B : "
    f"{result.consensus['away'] * 100:.2f}%"
)

print()

print("RISQUE")
print("-----------------------------------------------")

print(
    f"Confiance : "
    f"{result.risk['confidence'] * 100:.2f}%"
)

print(
    f"Niveau : "
    f"{result.risk['risk_level']}"
)

print()

print("================================================")