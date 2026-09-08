from engines.monte_carlo import simulate_match


HOME_LAMBDA = 1.8
AWAY_LAMBDA = 1.2
SIMULATIONS = 10000


result = simulate_match(
    home_lambda=HOME_LAMBDA,
    away_lambda=AWAY_LAMBDA,
    simulations=SIMULATIONS,
)


print()
print("==============================================")
print("      NORYX - MONTE CARLO ENGINE")
print("==============================================")
print()

print(
    f"Lambda domicile : {HOME_LAMBDA}"
)

print(
    f"Lambda extérieur : {AWAY_LAMBDA}"
)

print(
    f"Nombre de simulations : {SIMULATIONS}"
)

print()

print("RÉSULTATS")
print("----------------------------------------------")

print(
    f"Victoire Team A : "
    f"{result['home_win'] * 100:.2f}%"
)

print(
    f"Match nul : "
    f"{result['draw'] * 100:.2f}%"
)

print(
    f"Victoire Team B : "
    f"{result['away_win'] * 100:.2f}%"
)

print()

total = (
    result["home_win"]
    + result["draw"]
    + result["away_win"]
)

print(
    f"Total : "
    f"{total * 100:.2f}%"
)

print()

print("==============================================")