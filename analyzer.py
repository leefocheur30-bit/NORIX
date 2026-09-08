from data.match import Match

from engines.poisson import (
    analyze_match as analyze_poisson,
    calculate_1x2,
    find_best_score,
)

from engines.elo import (
    analyze_match as analyze_elo,
)

from engines.monte_carlo import (
    simulate_match,
)

from engines.consensus import (
    calculate_consensus,
    calculate_agreement,
)

from engines.risk import (
    calculate_risk,
)

from analysis.result import AnalysisResult


def analyze(match: Match) -> AnalysisResult:
    """
    Exécute les moteurs NORYX et rassemble
    tous les résultats dans AnalysisResult.
    """

    # ==========================================
    # POISSON
    # ==========================================

    poisson_results = analyze_poisson(match)

    poisson_1x2 = calculate_1x2(
        poisson_results
    )

    best_score_result = find_best_score(
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
    # CONSENSUS
    # ==========================================

    consensus_result = calculate_consensus(
        poisson_1x2,
        elo_result,
    )

    # ==========================================
    # ACCORD
    # ==========================================

    agreement_result = calculate_agreement(
        poisson_1x2,
        elo_result,
    )

    # ==========================================
    # RISQUE
    # ==========================================

    risk_result = calculate_risk(
        consensus_result,
        agreement_result["score"],
    )

    # ==========================================
    # RESULTAT COMPLET
    # ==========================================

    return AnalysisResult(
        match=match,

        poisson=poisson_1x2,

        elo=elo_result,

        monte_carlo=monte_carlo_result,

        consensus=consensus_result,

        risk=risk_result,

        best_score=best_score_result["score"],

        best_score_probability=(
            best_score_result["probability"]
        ),
    )