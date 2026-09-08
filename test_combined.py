from data.match import Match

from engines.poisson import (
    analyze_match as analyze_poisson,
    calculate_1x2 as poisson_1x2,
    find_best_score,
)

from engines.elo import (
    analyze_match as analyze_elo,
)

from engines.monte_carlo import (
    simulate_match,
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


# ==========================================
# POISSON
# ==========================================

poisson_results = analyze_poisson(match)

poisson_result_1x2 = poisson_1x2(
    poisson_results
)

best_score = find_best_score(
    poisson_results
)


# ==========================================
# ELO
# ==========================================

elo_result = analyze_elo(match)


# ==========================================
# MONTE CARLO
# ==========================================

monte_carlo_result = simulate_match(
    home_lambda=match.home_goals_avg,
    away_lambda=match.away_goals_avg,
    simulations=10000,
)


# ==========================================
# AFFICHAGE
# ==========================================

print()
print("================================================")
print("        NORYX - 3 MOTEURS COMBINÉS")
print("================================================")
print()

print(
    f"Match : {match.home_team} "
    f"vs {match.away_team}"
)

print()

print("1. POISSON")
print("------------------------------------------------")

print(
    f"Victoire {match.home_team} : "
    f"{poisson_result_1x2['home_win'] * 100:.2f}%"
)

print(
    f"Nul : "
    f"{poisson_result_1x2['draw'] * 100:.2f}%"
)

print(
    f"Victoire {match.away_team} : "
    f"{poisson_result_1x2['away_win'] * 100:.2f}%"
)

print(
    f"Score principal : "
    f"{best_score['score']}"
)

print()

print("2. ELO")
print("------------------------------------------------")

print(
    f"{match.home_team} : "
    f"{elo_result['home'] * 100:.2f}%"
)

print(
    f"{match.away_team} : "
    f"{elo_result['away'] * 100:.2f}%"
)

print()

print("3. MONTE CARLO")
print("------------------------------------------------")

print(
    f"Victoire {match.home_team} : "
    f"{monte_carlo_result['home_win'] * 100:.2f}%"
)

print(
    f"Nul : "
    f"{monte_carlo_result['draw'] * 100:.2f}%"
)

print(
    f"Victoire {match.away_team} : "
    f"{monte_carlo_result['away_win'] * 100:.2f}%"
)

print()

print("================================================")
print("              FIN DE L'ANALYSE")
print("================================================")