import os
from dotenv import load_dotenv

load_dotenv()

SPORTS_API_KEY = os.getenv("SPORTS_API_KEY")
SPORTS_API_URL = os.getenv("SPORTS_API_URL", "https://v3.football.api-sports.io")

# Autres paramètres
HOME_ADVANTAGE = 50
ELO_K_FACTOR = 20
MONTE_CARLO_SIMULATIONS = 10000
SCHEDULER_INTERVAL_MINUTES = 1
ENVIRONMENT = "development"