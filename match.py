# data/match.py
class Match:
    def __init__(self, home_team, away_team, home_elo=1500, away_elo=1500,
                 home_goals_avg=1.2, away_goals_avg=1.1, home_rank=10, away_rank=10):
        self.home_team = home_team
        self.away_team = away_team
        self.home_elo = home_elo
        self.away_elo = away_elo
        self.home_goals_avg = home_goals_avg
        self.away_goals_avg = away_goals_avg
        self.home_rank = home_rank
        self.away_rank = away_rank