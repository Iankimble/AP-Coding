from helperLogic import get_team_records, get_advanced_team_records, get_position_columns, get_season_Results_By_team , weeklyPlayerStats
import matplotlib.pyplot as plt

# Columns available to research based on year and position
# columnData = get_position_columns(2024, "QB")

'1. How much does QB pass accuracy influence team wins ? '
teamRecord = get_team_records(2024)
#print(teamRecord)

advanceStats =  get_advanced_team_records(2024)
print(advanceStats)

qbData = weeklyPlayerStats(2024, 'QB')
#print(qbData)

'2. Does defensive turnovers contribute to a teams win percentage ? '

'3. Who has the most passing yards of all time ? '