from engines.lambda_engine import LambdaEngine


def main():

    print("=" * 55)
    print("        TEST NORYX - LAMBDA ENGINE")
    print("=" * 55)
    print()

    # Statistiques fictives uniquement pour le test.
    class Statistics:
        def __init__(
            self,
            goals_for_avg,
            goals_against_avg
        ):
            self.goals_for_avg = goals_for_avg
            self.goals_against_avg = goals_against_avg

    home = Statistics(
        goals_for_avg=1.80,
        goals_against_avg=1.00,
    )

    away = Statistics(
        goals_for_avg=1.20,
        goals_against_avg=1.60,
    )

    engine = LambdaEngine()

    result = engine.calculate(
        home_statistics=home,
        away_statistics=away,
    )

    print("STATISTIQUES")
    print("-" * 55)

    print(
        f"Buts domicile marqués   : "
        f"{home.goals_for_avg:.2f}"
    )

    print(
        f"Buts domicile encaissés : "
        f"{home.goals_against_avg:.2f}"
    )

    print(
        f"Buts extérieur marqués  : "
        f"{away.goals_for_avg:.2f}"
    )

    print(
        f"Buts extérieur encaissés: "
        f"{away.goals_against_avg:.2f}"
    )

    print()
    print("LAMBDA NORYX")
    print("-" * 55)

    print(
        f"Lambda domicile : "
        f"{result['home_lambda']:.3f}"
    )

    print(
        f"Lambda extérieur : "
        f"{result['away_lambda']:.3f}"
    )

    print(
        f"Lambda total : "
        f"{result['total_lambda']:.3f}"
    )

    print()
    print("=" * 55)
    print("TEST RÉUSSI")
    print("=" * 55)


if __name__ == "__main__":
    main()