from engines.fusion import NoryxFusion


def main():

    print("=" * 60)
    print("          TEST NORYX - FUSION")
    print("=" * 60)
    print()

    poisson = {
        "home": 0.55,
        "draw": 0.23,
        "away": 0.22,
    }

    elo = {
        "home": 0.50,
        "draw": 0.25,
        "away": 0.25,
    }

    monte_carlo = {
        "home": 0.53,
        "draw": 0.24,
        "away": 0.23,
    }

    consensus = {
        "home": 0.52,
        "draw": 0.25,
        "away": 0.23,
    }

    fusion = NoryxFusion()

    result = fusion.combine(
        poisson=poisson,
        elo=elo,
        monte_carlo=monte_carlo,
        consensus=consensus,
    )

    prediction = fusion.best_prediction(result)

    print("FUSION 1X2")
    print("-" * 60)

    print(
        f"Victoire domicile : "
        f"{result['home'] * 100:.2f}%"
    )

    print(
        f"Nul               : "
        f"{result['draw'] * 100:.2f}%"
    )

    print(
        f"Victoire extérieur : "
        f"{result['away'] * 100:.2f}%"
    )

    print()

    print("PRÉDICTION FINALE")
    print("-" * 60)

    print(
        f"Pronostic : "
        f"{prediction['prediction']}"
    )

    print(
        f"Probabilité : "
        f"{prediction['probability'] * 100:.2f}%"
    )

    print()

    total = sum(result.values())

    print(
        f"Contrôle somme : "
        f"{total:.6f}"
    )

    print()

    if abs(total - 1.0) < 0.000001:
        print("=" * 60)
        print("TEST RÉUSSI")
        print("=" * 60)
    else:
        print("=" * 60)
        print("TEST ÉCHOUÉ")
        print("=" * 60)


if __name__ == "__main__":
    main()