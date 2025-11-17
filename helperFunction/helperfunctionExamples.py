from helperLogic import get_team_records,compare_two_teams_points, weeklyPlayerStats, get_advanced_team_records, get_position_columns, get_season_Results_By_team, plot_player_stat, plot_weekly_player_stats, get_position_columns,get_player_stats_by_name, plot_player_stat
import matplotlib.pyplot as plt

# Returns all available statistics for any position based on year.
columns = get_position_columns(2024, 'WR')
print(columns)
# Returns team records, wins, losses, and scores based on year
# note- all data is capped at 2024
records = get_team_records(2022)

# Returns team data for their entire season
teamSeason = get_season_Results_By_team(2024, 'PHI') 

# Returns weekly player stats based on year and position arguments 
stats = weeklyPlayerStats(2024, "WR")  
print(stats)
# Returns player stats based on named, position and week(optional)
# When passing a player name, use their first initial followed by their last name
hurts_week3 = get_player_stats_by_name(2024, "J.Hurts", "QB", week=3)

# returns data for specific pl
# showPlayerChart= plot_player_stat(stats, "receiving_first_downs","WR receiving data")

# returns advanced states for teams based on year
advanceStates = get_advanced_team_records(2024)

# visually compares two teams based on the seasonal data
team_games = get_team_records(2024)
#phiVsDal = compare_two_teams_points(team_games, "PHI","DAL")
