from helperFunctions import get_season_totals_by_position, plot_position_stat_bar, plot_player_stat_by_week, get_player_stats

# 1. What 4 stats makes a player washed? 
# games played - indicates the player is healhy or game day ready
# attempts - indicates they are able to get the ball out
# completions -  they are getting the ball to their recievers
# passing yards - they are getting significant yardage


# Get all player stats from 2024
qbStats= get_season_totals_by_position(2024,'QB')
print(qbStats)

# 2. Why is this player washed? 
# Based on the league average for rushing yard for the qb position, russell wilson...

RussStats = get_player_stats(2024,'Russell','Wilson')

#Line graph of Russ stats for 2024
plot_player_stat_by_week(2024, 'Russell','Wilson',"passing_yards", save_path='Jalen Hurts Passing Yards 2024')

