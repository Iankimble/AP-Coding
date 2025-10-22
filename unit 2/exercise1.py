import pandas as pd
import nfl_data_py as nfl

from helperFunctions import get_team_records, get_season_Results_By_team

# schedules = nfl.import_schedules([2024])
 
# print(schedules.columns.tolist())

records = get_team_records(2025)


birds = get_season_Results_By_team(2025,'NYJ')
print(birds)
pd =[ 4, 3, 7, 6, -4,  -17]

# COLTS AND BUCS FOR HIGHEST PD
# COLTS 78
# TAMPA 14


















# 'What is the highest point differential for the eagles ?'
# 'What is the highest point differential in the league this season? '
# 'What is the lowest point differential in the league this season? '

# 'Point Differential=Points For Points Against'

# 'Points For (PF) = total points the team has scored.'

# 'Points Against (PA) = total points the team has allowed'







#  print(records[['team','points_for', 'points_against']])

# print(records[['wins']].mean()) # what was the average wins for the years

# Find a season where the average wins was below 8.0 in the last 10 years ? 

# 2022 - 8.4 wins 
# 2020 - 7.9 wins 

# 1. Find at least 2 teams that have average of at least 12 wins over 
# the past 5 seasons

# Cheif and Bills













# 2. What is the median wins for teams over the past 5 seasons.

# - points for = how many points a team scored on opponents
# - points allowed = how may points a team allowed by opponents

# 3. What team had the highest points scored this past season- whwat was there record
# print(records[['team','points_for']].max()) # notation for getting specfic columns

# 4. What team had the least amount scored this past season - what was there record
# print(records[['team','points_for']].min()) # notation for getting specfic columns

# which team has the highest and lowest point differential? What were their records?

# Do you think a team can score a lot of points but still lose games? Why?

# Do teams with more wins always have more points_for?

# what is the average points for scored in the nfl and how many teams are above the average
