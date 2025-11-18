from helperLogic import get_player_stats_by_name, plot_weekly_player_stats,plot_player_stat, get_team_records, get_advanced_team_records, get_position_columns, get_season_Results_By_team , weeklyPlayerStats
import matplotlib.pyplot as plt

# Columns available to research based on year and position
columnData = get_position_columns(2024, "QB")
# print(columnData)

'1. How much does QB pass accuracy influence team wins ? '
teamRecord = get_team_records(2024)
print(teamRecord)

qbData = weeklyPlayerStats(2024, 'QB')
print(qbData)
# qbData = weeklyPlayerStats(2024, 'QB')
# qb_pcar = plot_player_stat(qbData,"pacr","qb pacr")

'J.Allen'
'J.Hurts'

playerStat= get_player_stats_by_name(2024,'J.Hurts','QB')
print(playerStat)

'we want to find a relationship between completion % and wins'
'accuracy = completions %'
'wins = '
'top 5: '

'Answer: Yes, there is a relationship. based on the average qb completion %, anything above 60 % is considered a good completion number'
"also based on team records, the top 10- top teams all have had qbs that have over 65% completion percentages."

advanceStats =  get_advanced_team_records(2024)
#print(advanceStats)

# qbData = weeklyPlayerStats(2024, 'QB')
#print(qbData)

'2. Does defensive turnovers contribute to a teams win percentage ? '

'3. Who has the most passing yards of all time ? '