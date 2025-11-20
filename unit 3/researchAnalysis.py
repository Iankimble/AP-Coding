from helperLogic import get_season_Results_By_team, get_player_stats_by_name,get_advanced_team_records, plot_weekly_player_stats,plot_player_stat, get_team_records, get_advanced_team_records, get_position_columns, get_season_Results_By_team , weeklyPlayerStats
import matplotlib.pyplot as plt

# Create a new document called researchAnalysis.py and answer the following research prompts. 
# Your answer should include the following:

# Describe what type of research question the prompt is and explain why. 
# Explain which helper functions you used and how you came to your answer. 

#1. Which division had the strongest defense based on yards allowed per game in 2024?
teamData = get_advanced_team_records(2024)
# print(teamData)

teamRes = get_season_Results_By_team(2024,'PHI')
# print(teamRes)

#2. Which WR had the most targets vs their receptions (catches) in 2024?

#3. Does time of possession strongly correlate with wins in 2024?
