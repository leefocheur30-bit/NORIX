from engines.risk import RiskEngine


def main():
    print("=" * 60)
    print("       TEST NORYX - RISK ENGINE")
    print("=" * 60)

    probabilities = {
        "home": 0.62,
        "draw": 0.21,
        "away": 0.17,
    }

    agreement_score = 1.0

    engine = RiskEngine()

    result = engine.calculate(
        probabilities,
        agreement_score
    )

    print()
    print("PROBABILITÉS")
    print("-" * 60)
    print(f"1 : {probabilities['home']:.2%}")
    print(f"X : {probabilities['draw']:.2%}")
    print(f"2 : {probabilities['away']:.2%}")

    print()
    print("ANALYSE DU RISQUE")
    print("-" * 60)
    print(f"Prédiction      : {result['prediction']}")
    print(f"Probabilité     : {result['probability']:.2%}")
    print(f"Marge           : {result['margin']:.2%}")
    print(f"Accord moteurs  : {result['agreement_score']:.2%}")
    print(f"Confiance       : {result['confidence']:.2%}")
    print(f"Niveau de risque: {result['risk_level']}")
    print(f"Signal          : {result['signal']}")

    print()
    print("=" * 60)
    print("TEST TERMINÉ")
    print("=" * 60)


if __name__ == "__main__":
    main()