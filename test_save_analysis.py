from database.database import Base, engine

from database.repository import (
    save_analysis,
    get_all_analyses,
)

from data.match import Match

from analysis.analyzer import analyze


# ==========================================
# CRÉER LES TABLES
# ==========================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================
# CRÉER UN MATCH
# ==========================================

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
# ANALYSER
# ==========================================

result = analyze(match)


# ==========================================
# SAUVEGARDER
# ==========================================

analysis_id = save_analysis(
    result
)


# ==========================================
# AFFICHAGE
# ==========================================

print()
print("==============================================")
print("       NORYX - SAVE ANALYSIS TEST")
print("==============================================")
print()

print(
    f"Match : "
    f"{result.match.home_team} "
    f"vs {result.match.away_team}"
)

print()

print(
    f"Meilleur score : "
    f"{result.best_score}"
)

print(
    f"Probabilité : "
    f"{result.best_score_probability * 100:.2f}%"
)

print()

print(
    f"Consensus Team A : "
    f"{result.consensus['home'] * 100:.2f}%"
)

print(
    f"Consensus Nul : "
    f"{result.consensus['draw'] * 100:.2f}%"
)

print(
    f"Consensus Team B : "
    f"{result.consensus['away'] * 100:.2f}%"
)

print()

print(
    f"Confiance : "
    f"{result.risk['confidence'] * 100:.2f}%"
)

print(
    f"Risque : "
    f"{result.risk['risk_level']}"
)

print()

print(
    f"✅ Analyse enregistrée avec ID : "
    f"{analysis_id}"
)

print()

# ==========================================
# VÉRIFICATION
# ==========================================

analyses = get_all_analyses()

print(
    f"Nombre total d'analyses dans la base : "
    f"{len(analyses)}"
)

print()

print("==============================================")