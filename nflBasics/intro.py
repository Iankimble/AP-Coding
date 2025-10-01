# step 1. import code libraries to help us
import nfl_data_py as nfl
import pandas as pd
import os 

# step 2. test path to make sure we are accessing the 
# nfl csv data. 
path = os.path.abspath("nflData/nfl_records_2024.csv")

records = pd.read_csv(path)
# print(records.head())
# print(records.columns)

teams = nfl.import_team_desc()
team_stats =nfl.import_seasonal_data([2024])

standings = nfl.import_win_totals([2024])

# print(teams)
# print(team_stats.columns)

# Suppose the CSV has columns "team", "wins", "losses"
top5 = records.sort_values(by=["wins", "losses"], ascending=[False, True])
print(top5[["team", "wins", "losses"]].head(5))

teams = nfl.import_team_desc()
top5 = top5.merge(teams, on="team", how="left")
print(top5[["team_name", "wins", "losses"]].head(5))

# bestRecord = team_stats.sort_values(by= "wins", ascending= False)
# print(bestRecord[['team','wins','losses']].head())