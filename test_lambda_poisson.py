from engines.lambda_engine import LambdaEngine
from engines.poisson import (
    analyze_match,
    find_best_score,
    calculate_1x2,
    calculate_distribution_coverage,
)
from data.match import Match


class Statistics:
    def __init__(self, goals_for_avg, goals_against_avg):
        self.goals_for_avg = goals_for_avg
        self.goals_against_avg = goals_against_avg


def main():

    print("=" * 60)
    print("       TEST NORYX - LAMBDA + POISSON")
    print("=" * 60)
    print()

    # ==================================================
    # STATISTIQUES DES ÉQUIPES
    # ==================================================

    home_statistics = Statistics(
        goals_for_avg=1.80,
        goals_against_avg=1.00,
    )

    away_statistics = Statistics(
        goals_for_avg=1.20,
        goals_against_avg=1.60,
    )

    print("STATISTIQUES")
    print("-" * 60)

    print(
        f"Buts domicile marqués   : "
        f"{home_statistics.goals_for_avg:.2f}"
    )

    print(
        f"Buts domicile encaissés : "
        f"{home_statistics.goals_against_avg:.2f}"
    )

    print(
        f"Buts extérieur marqués  : "
        f"{away_statistics.goals_for_avg:.2f}"
    )

    print(
        f"Buts extérieur encaissés: "
        f"{away_statistics.goals_against_avg:.2f}"
    )

    print()

    # ==================================================
    # CALCUL DES LAMBDA
    # ==================================================

    lambda_engine = LambdaEngine()

    lambdas = lambda_engine.calculate(
        home_statistics=home_statistics,
        away_statistics=away_statistics,
    )

    home_lambda = lambdas["home_lambda"]
    away_lambda = lambdas["away_lambda"]

    print("LAMBDA NORYX")
    print("-" * 60)

    print(
        f"Lambda domicile  : {home_lambda:.3f}"
    )

    print(
        f"Lambda extérieur : {away_lambda:.3f}"
    )

    print(
        f"Lambda total     : "
        f"{lambdas['total_lambda']:.3f}"
    )

    print()

    # ==================================================
    # CRÉATION DU MATCH
    # ==================================================

    match = Match(
        home_team="Team A",
        away_team="Team B",

        home_elo=1500,
        away_elo=1500,

        home_goals_avg=home_lambda,
        away_goals_avg=away_lambda,

        home_rank=10,
        away_rank=10,
    )

    # ==================================================
    # POISSON
    # ==================================================

    results = analyze_match(match)

    print("POISSON")
    print("-" * 60)

    print(
        f"Nombre de scores calculés : "
        f"{len(results)}"
    )

    print()

    # ==================================================
    # MEILLEUR SCORE
    # ==================================================

    best_score = find_best_score(results)

    print("SCORE EXACT")
    print("-" * 60)

    print(
        f"Meilleur score : "
        f"{best_score['score']}"
    )

    print(
        f"Probabilité : "
        f"{best_score['probability'] * 100:.2f}%"
    )

    print()

    # ==================================================
    # 1X2
    # ==================================================

    probabilities = calculate_1x2(results)

    print("PROBABILITÉS 1X2")
    print("-" * 60)

    print(
        f"Victoire domicile : "
        f"{probabilities['home_win'] * 100:.2f}%"
    )

    print(
        f"Nul               : "
        f"{probabilities['draw'] * 100:.2f}%"
    )

    print(
        f"Victoire extérieur : "
        f"{probabilities['away_win'] * 100:.2f}%"
    )

    print()

    # ==================================================
    # COUVERTURE
    # ==================================================

    coverage = calculate_distribution_coverage(
        results
    )

    print("COUVERTURE")
    print("-" * 60)

    print(
        f"Capturée : "
        f"{coverage['total'] * 100:.4f}%"
    )

    print(
        f"Ignorée  : "
        f"{coverage['ignored'] * 100:.4f}%"
    )

    print()

    # ==================================================
    # VALIDATION
    # ==================================================

    if (
        home_lambda > 0
        and away_lambda > 0
        and len(results) == 121
        and 0 <= coverage["total"] <= 1
    ):
        print("=" * 60)
        print("TEST RÉUSSI")
        print("=" * 60)
    else:
        print("=" * 60)
        print("TEST ÉCHOUÉ")
        print("=" * 60)


if __name__ == "__main__":
    main()