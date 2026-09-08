from data.match import Match

from analysis.analyzer import analyze

from reports.generator import generate_report


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


result = analyze(match)


report = generate_report(result)


print(report)