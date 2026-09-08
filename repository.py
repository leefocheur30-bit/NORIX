from database.database import SessionLocal
from database.models import AnalysisModel


def save_analysis(
    result,
):
    """
    Sauvegarde un AnalysisResult complet
    dans la base NORYX.
    """

    session = SessionLocal()

    try:

        analysis = AnalysisModel(
            home_team=result.match.home_team,
            away_team=result.match.away_team,

            home_probability=result.consensus["home"],
            draw_probability=result.consensus["draw"],
            away_probability=result.consensus["away"],

            best_score=result.best_score,
            best_score_probability=(
                result.best_score_probability
            ),

            poisson_home=result.poisson["home_win"],
            poisson_draw=result.poisson["draw"],
            poisson_away=result.poisson["away_win"],

            elo_home=result.elo["home"],
            elo_away=result.elo["away"],

            monte_carlo_home=(
                result.monte_carlo["home_win"]
            ),
            monte_carlo_draw=(
                result.monte_carlo["draw"]
            ),
            monte_carlo_away=(
                result.monte_carlo["away_win"]
            ),

            confidence=result.risk["confidence"],
            risk_level=result.risk["risk_level"],
        )

        session.add(analysis)
        session.commit()
        session.refresh(analysis)

        return analysis.id

    finally:

        session.close()


def get_all_analyses():

    session = SessionLocal()

    try:

        return (
            session.query(AnalysisModel)
            .order_by(
                AnalysisModel.created_at.desc()
            )
            .all()
        )

    finally:

        session.close()