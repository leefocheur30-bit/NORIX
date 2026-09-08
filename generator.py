from analysis.result import AnalysisResult


def generate_report(result: AnalysisResult) -> str:
    """
    Transforme une analyse NORYX en rapport texte.
    """

    match = result.match

    home_probability = (
        result.consensus["home"] * 100
    )

    draw_probability = (
        result.consensus["draw"] * 100
    )

    away_probability = (
        result.consensus["away"] * 100
    )

    confidence = (
        result.risk["confidence"] * 100
    )

    risk_level = result.risk["risk_level"]

    if (
        home_probability >= draw_probability
        and home_probability >= away_probability
    ):
        favorite = match.home_team

    elif away_probability >= draw_probability:
        favorite = match.away_team

    else:
        favorite = "Match nul"

    report = f"""
==================================================
                 NORYX BOT
              ANALYSE DU MATCH
==================================================

⚽ MATCH
{match.home_team} vs {match.away_team}

--------------------------------------------------
📊 CONSENSUS NORYX
--------------------------------------------------

Victoire {match.home_team} : {home_probability:.2f}%
Match nul                : {draw_probability:.2f}%
Victoire {match.away_team} : {away_probability:.2f}%

--------------------------------------------------
🏆 FAVORI
--------------------------------------------------

{favorite}

--------------------------------------------------
🧠 CONFIANCE
--------------------------------------------------

{confidence:.2f}%

--------------------------------------------------
⚠️ RISQUE
--------------------------------------------------

{risk_level}

--------------------------------------------------
🔬 MOTEURS UTILISÉS
--------------------------------------------------

✓ Poisson
✓ ELO
✓ Monte Carlo
✓ Consensus
✓ Risk

==================================================
        Les probabilités sont des estimations.
==================================================
"""

    return report