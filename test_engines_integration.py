from engines.elo import analyze_match as analyze_elo
from engines.monte_carlo import simulate_match
from engines.consensus import (
    calculate_consensus,
    calculate_agreement,
)
from engines.poisson import (
    analyze_match as analyze_poisson,
    calculate_1x2,
)
from engines.fusion import NoryxFusion
from data.match import Match


def main():

    print("=" * 65)
    print("       TEST NORYX - INTEGRATION DES MOTEURS")
    print("=" * 65)
    print()

    # ==================================================
    # MATCH
    # ==================================================

    match = Match(
        home_team="Team A",
        away_team="Team B",

        home_elo=1500,
        away_elo=1450,

        home_goals_avg=1.87,
        away_goals_avg=1.10,

        home_rank=5,
        away_rank=10,
    )

    # ==================================================
    # POISSON
    # ==================================================

    poisson_results = analyze_poisson(match)

    poisson = calculate_1x2(
        poisson_results
    )

    print("POISSON")
    print("-" * 65)

    print(
        f"Domicile : "
        f"{poisson['home_win'] * 100:.2f}%"
    )

    print(
        f"Nul      : "
        f"{poisson['draw'] * 100:.2f}%"
    )

    print(
        f"Extérieur: "
        f"{poisson['away_win'] * 100:.2f}%"
    )

    print()

    # ==================================================
    # ELO
    # ==================================================

    elo_raw = analyze_elo(match)

    # ELO ne calcule pas directement le nul.
    # On transforme donc sa sortie en distribution
    # compatible avec la fusion.
    #
    # Le nul est volontairement neutre ici.
    # Il sera principalement déterminé par Poisson
    # et Monte-Carlo.

    elo = {
        "home": elo_raw["home"],
        "draw": 0.0,
        "away": elo_raw["away"],
    }

    print("ELO")
    print("-" * 65)

    print(
        f"Domicile : "
        f"{elo['home'] * 100:.2f}%"
    )

    print(
        f"Extérieur: "
        f"{elo['away'] * 100:.2f}%"
    )

    print()

    # ==================================================
    # MONTE-CARLO
    # ==================================================

    monte_carlo = simulate_match(
        home_lambda=match.home_goals_avg,
        away_lambda=match.away_goals_avg,
    )

    print("MONTE-CARLO")
    print("-" * 65)

    print(
        f"Domicile : "
        f"{monte_carlo['home_win'] * 100:.2f}%"
    )

    print(
        f"Nul      : "
        f"{monte_carlo['draw'] * 100:.2f}%"
    )

    print(
        f"Extérieur: "
        f"{monte_carlo['away_win'] * 100:.2f}%"
    )

    print()

    # ==================================================
    # CONSENSUS
    # ==================================================

    consensus = calculate_consensus(
        poisson=poisson,
        elo={
            "home": elo_raw["home"],
            "away": elo_raw["away"],
        },
    )

    agreement = calculate_agreement(
        poisson=poisson,
        elo={
            "home": elo_raw["home"],
            "away": elo_raw["away"],
        },
    )

    print("CONSENSUS")
    print("-" * 65)

    print(
        f"Domicile : "
        f"{consensus['home'] * 100:.2f}%"
    )

    print(
        f"Nul      : "
        f"{consensus['draw'] * 100:.2f}%"
    )

    print(
        f"Extérieur: "
        f"{consensus['away'] * 100:.2f}%"
    )

    print(
        f"Accord moteurs : "
        f"{agreement['status']}"
    )

    print()

    # ==================================================
    # FUSION
    # ==================================================

    fusion = NoryxFusion()

    fusion_result = fusion.combine(
        poisson={
            "home": poisson["home_win"],
            "draw": poisson["draw"],
            "away": poisson["away_win"],
        },

        elo=elo,

        monte_carlo={
            "home": monte_carlo["home_win"],
            "draw": monte_carlo["draw"],
            "away": monte_carlo["away_win"],
        },

        consensus=consensus,
    )

    prediction = fusion.best_prediction(
        fusion_result
    )

    print("FUSION NORYX")
    print("-" * 65)

    print(
        f"Domicile : "
        f"{fusion_result['home'] * 100:.2f}%"
    )

    print(
        f"Nul      : "
        f"{fusion_result['draw'] * 100:.2f}%"
    )

    print(
        f"Extérieur: "
        f"{fusion_result['away'] * 100:.2f}%"
    )

    print()

    print("PRÉDICTION FINALE")
    print("-" * 65)

    print(
        f"Pronostic : "
        f"{prediction['prediction']}"
    )

    print(
        f"Confiance : "
        f"{prediction['probability'] * 100:.2f}%"
    )

    print()

    # ==================================================
    # VALIDATION
    # ==================================================

    total = sum(
        fusion_result.values()
    )

    print(
        f"Contrôle somme : "
        f"{total:.6f}"
    )

    print()

    if abs(total - 1.0) < 0.000001:

        print("=" * 65)
        print("TEST RÉUSSI")
        print("=" * 65)

    else:

        print("=" * 65)
        print("TEST ÉCHOUÉ")
        print("=" * 65)


if __name__ == "__main__":
    main()