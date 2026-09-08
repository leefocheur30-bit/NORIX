from data.match import Match

from engines.elo import (
    analyze_match,
    update_ratings,
)


def test_probabilities_are_valid(result):
    """
    Vérifie que les probabilités ELO
    sont comprises entre 0 et 1.
    """

    assert 0 <= result["home"] <= 1
    assert 0 <= result["away"] <= 1


def test_probabilities_total_100(result):
    """
    Vérifie que les deux probabilités
    totalisent 100 %.
    """

    total = result["home"] + result["away"]

    assert abs(total - 1.0) < 0.000001


def test_home_win_increases_home_rating(
    home_elo,
    away_elo,
):
    """
    Une victoire à domicile doit augmenter
    le rating de l'équipe à domicile.
    """

    result = update_ratings(
        home_elo=home_elo,
        away_elo=away_elo,
        home_result=1.0,
    )

    assert result["home_elo"] > home_elo
    assert result["away_elo"] < away_elo


def test_home_loss_decreases_home_rating(
    home_elo,
    away_elo,
):
    """
    Une défaite à domicile doit diminuer
    le rating de l'équipe à domicile.
    """

    result = update_ratings(
        home_elo=home_elo,
        away_elo=away_elo,
        home_result=0.0,
    )

    assert result["home_elo"] < home_elo
    assert result["away_elo"] > away_elo


def test_elo_points_are_conserved(
    home_elo,
    away_elo,
):
    """
    Vérifie que la variation du rating
    de l'une est l'inverse de celle de l'autre.
    """

    result = update_ratings(
        home_elo=home_elo,
        away_elo=away_elo,
        home_result=1.0,
    )

    home_change = result["home_elo"] - home_elo
    away_change = result["away_elo"] - away_elo

    assert abs(home_change + away_change) < 0.000001


if __name__ == "__main__":

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

    probabilities = analyze_match(match)

    print()
    print("==============================================")
    print("          TESTS AUTOMATIQUES ELO")
    print("==============================================")
    print()

    try:

        test_probabilities_are_valid(
            probabilities
        )

        print("✅ Probabilités valides")

        test_probabilities_total_100(
            probabilities
        )

        print("✅ Probabilités = 100 %")

        test_home_win_increases_home_rating(
            match.home_elo,
            match.away_elo,
        )

        print("✅ Victoire → rating domicile augmente")

        test_home_loss_decreases_home_rating(
            match.home_elo,
            match.away_elo,
        )

        print("✅ Défaite → rating domicile diminue")

        test_elo_points_are_conserved(
            match.home_elo,
            match.away_elo,
        )

        print("✅ Conservation des points ELO")

        print()
        print("🎉 TOUS LES TESTS ELO SONT RÉUSSIS !")
        print()

    except AssertionError:

        print()
        print("❌ UN TEST ELO A ÉCHOUÉ")
        print()