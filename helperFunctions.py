import pandas as pd
import nfl_data_py as nfl

# Load 2024 NFL schedule data
schedules = nfl.import_schedules([2024])
weeklyStats = nfl.import_weekly_data([2024])
pbp = nfl.import_pbp_data([2024])

def get_team_records(year):
    games = nfl.import_schedules([year])

    if "season_type" in games.columns:
        games = games[games["season_type"] == "REG"]
    else:
        games = games[games["game_type"] == "REG"]

    games = games.dropna(subset=["home_score", "away_score"])

    home = games[["home_team", "home_score", "away_score"]].rename(
        columns={"home_team": "team", "home_score": "points_for", "away_score": "points_against"}
    )
    home["win"] = (home["points_for"] > home["points_against"]).astype(int)

    away = games[["away_team", "away_score", "home_score"]].rename(
        columns={"away_team": "team", "away_score": "points_for", "home_score": "points_against"}
    )
    away["win"] = (away["points_for"] > away["points_against"]).astype(int)

    all_games = pd.concat([home, away])

    records = all_games.groupby("team").agg(
        wins=("win", "sum"),
        losses=("win", lambda x: len(x) - x.sum()),
        points_for=("points_for", "sum"),
        points_against=("points_against", "sum")
    ).reset_index()

    records = records.sort_values("wins", ascending=False).reset_index(drop=True)

    return records

def get_season_Results_By_team(year, team):
    schedules = nfl.import_schedules([year])

    if "season_type" in schedules.columns:
        schedules = schedules[schedules["season_type"] == "REG"]
    else:
        schedules = schedules[schedules["game_type"] == "REG"]

    team_games = schedules[
        (schedules["home_team"] == team) | (schedules["away_team"] == team)
    ].copy()

    def get_result(row):
        if row["home_team"] == team:
            return "W" if row["home_score"] > row["away_score"] else "L"
        else:
            return "W" if row["away_score"] > row["home_score"] else "L"

    team_games["result"] = team_games.apply(get_result, axis=1)
    team_games["points_for"] = team_games.apply(
        lambda r: r["home_score"] if r["home_team"] == team else r["away_score"], axis=1
    )
    team_games["points_against"] = team_games.apply(
        lambda r: r["away_score"] if r["home_team"] == team else r["home_score"], axis=1
    )

    return team_games[["week", "home_team", "away_team", "points_for", "points_against", "result"]]
