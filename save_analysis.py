from data.match import Match

from analysis.analyzer import analyze

from database.database import Base, engine

from database.repository import save_analysis


# ==================================================
# CRÉER LES TABLES
# ==================================================

Base.metadata.create_all(
    bind=engine
)


# ==================================================
# MATCH
# ==================================================

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


# ==================================================
# ANALYSE NORYX
# ==================================================

result = analyze(match)


# ==================================================
# MEILLEUR SCORE
# ==================================================

best_score = max(
    result.poisson.items(),
    key=lambda item: item[1],
)