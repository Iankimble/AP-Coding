import pandas as pd
import nfl_data_py as nfl

# Load 2024 NFL schedule data
schedules = nfl.import_schedules([2024]) # schedule data
weeklyStats = nfl.import_weekly_data([2024]) # weekly game data
pbp = nfl.import_pbp_data([2024]) # game play by play data

# -- Shows all columns on object --
# print(pbp.columns.tolist()) 
# print(weeklyStats.columns) 
# print(schedules.columns)

team_schedule = schedules[
    (schedules["home_team"] == 'PHI') | (schedules["away_team"] == 'PHI')
]

# print(team_schedule)

schedules[["week", "home_team", "away_team", "home_score", "away_score"]] # query only select few columns

# print(regular_season)

# quick notes
# querying columns can have different column names do to WHEN it was uploaded - older data my have a different column name
# it can also be a result of WHERE it was queried from nflR



