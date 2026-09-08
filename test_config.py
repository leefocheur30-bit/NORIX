from config import (
    SPORTS_API_KEY,
    SPORTS_API_URL,
    MONTE_CARLO_SIMULATIONS,
    HOME_ADVANTAGE,
    ELO_K_FACTOR,
    SCHEDULER_INTERVAL_MINUTES,
    ENVIRONMENT,
)


print()
print("==============================================")
print("           NORYX - API CONFIG")
print("==============================================")
print()

print(
    "Clé API détectée :",
    bool(SPORTS_API_KEY)
)

print(
    "URL API :",
    SPORTS_API_URL
)

print(
    "Monte Carlo :",
    MONTE_CARLO_SIMULATIONS
)

print(
    "Avantage domicile :",
    HOME_ADVANTAGE
)

print(
    "ELO K-Factor :",
    ELO_K_FACTOR
)

print(
    "Scheduler :",
    SCHEDULER_INTERVAL_MINUTES,
    "minute(s)"
)

print(
    "Environnement :",
    ENVIRONMENT
)

print()

print("==============================================")