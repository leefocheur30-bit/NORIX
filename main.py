from data.match import Match


def main():

    print("================================")
    print("        NORYX BOT v0.2")
    print("================================")
    print()

    match = Match(
        home_team="Team A",
        away_team="Team B",
        home_goals_avg=1.8,
        away_goals_avg=1.2,
        home_rank=3,
        away_rank=7,
    )

    print(f"Match : {match.home_team} vs {match.away_team}")
    print()

    print(f"{match.home_team}")
    print(f"Buts moyens : {match.home_goals_avg}")
    print(f"Classement : {match.home_rank}")
    print()

    print(f"{match.away_team}")
    print(f"Buts moyens : {match.away_goals_avg}")
    print(f"Classement : {match.away_rank}")
    print()

    if match.home_goals_avg > match.away_goals_avg:
        print("Analyse NORYX :")
        print(
            f"{match.home_team} possède actuellement l'avantage."
        )

    else:
        print("Analyse NORYX :")
        print(
            f"{match.away_team} possède actuellement l'avantage."
        )


if __name__ == "__main__":
    main()