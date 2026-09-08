from database.database import Base, engine

from database.models import AnalysisModel

from database.repository import (
    save_analysis,
    get_all_analyses,
)


# Création des tables
Base.metadata.create_all(
    bind=engine
)


# Enregistrement d'une analyse de test
analysis_id = save_analysis(
    home_team="Team A",
    away_team="Team B",
    home_probability=0.55,
    draw_probability=0.23,
    away_probability=0.22,
    confidence=0.68,
    risk_level="MODÉRÉ",
)


print()
print("==============================================")
print("          NORYX - DATABASE TEST")
print("==============================================")
print()

print(
    f"Analyse enregistrée avec ID : "
    f"{analysis_id}"
)

print()

analyses = get_all_analyses()

print(
    f"Nombre d'analyses enregistrées : "
    f"{len(analyses)}"
)

print()

for analysis in analyses:

    print(
        f"{analysis.id} - "
        f"{analysis.home_team} vs "
        f"{analysis.away_team}"
    )

    print(
        f"Confiance : "
        f"{analysis.confidence * 100:.2f}%"
    )

    print(
        f"Risque : "
        f"{analysis.risk_level}"
    )

    print()

print("==============================================")