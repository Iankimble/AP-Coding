from helperLogic import get_player_stats_by_name,get_advanced_team_records, plot_weekly_player_stats,plot_player_stat, get_team_records, get_advanced_team_records, get_position_columns, get_season_Results_By_team , weeklyPlayerStats
import matplotlib.pyplot as plt

# Columns available to research based on year and position
columnData = get_position_columns(2024, "QB")
# print(columnData)

'1. How much does QB pass accuracy influence team wins ? '
teamRecord = get_team_records(2024)
#print(teamRecord)

qbData = weeklyPlayerStats(2024, 'QB')
#print(qbData)

'J.Allen'
'J.Hurts'

playerStat= get_player_stats_by_name(2024,'J.Hurts','QB')
#print(playerStat)

'Answer: Yes, there is a relationship. based on the average qb completion %, anything above 60 % is considered a good completion number'
"also based on team records, the top 10- top teams all have had qbs that have over 65% completion percentages."






# When asnswering the questions and recording your results, be sure to include 
# the following:
# Identify what type of question it is; is it comparative, descriptive 
# or relational, and explain why.
# Is the intial questionn clear, focused, measureable, and insight, explain why.
# which helper functions did you use and briefly explain why.
# finally, answer the question and describe why you feel as through your 
# answer is correct via your research and or explain why you need to change
# the intial question, if necessary.

# Descriptive = Summarizes and provides statistical context to some data.
# example = what factors contributed to the eagles win on Sunday

# Compparative = Comparing different groups of data
# example = how does the ravens offense compare to the offense of 
# their divisional rivals

# Relational = Find relationships or patterns in data
# example = is there a pattern special team kick returns and playoff performance?

# Please write responses as a string data type
'2.Q: Does defensive turnovers contribute to a teams win percentage ? '
'3.Q: Who has the most passing yards of all time ? '

adv =get_advanced_team_records(2024)
print(adv)