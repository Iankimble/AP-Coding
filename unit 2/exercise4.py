from helperFunctions import weeklyPlayerStats, plot_player_stat, plot_weekly_player_stats, get_position_columns,get_player_stats_by_name
import matplotlib.pyplot as plt

stats = weeklyPlayerStats(2024, "WR")  
#print(stats)

# plot_player_stat(stats, stat="rush_ypc", top_n=5, title="rb rushing per carry (2024)", save_path="RB_rushing_pyc_2024.png"  )

# You can copy and paste this code from the AP repo. the document is called exercise4.py
# in the unit2 folder. 

# Try to run the code above.

# If you have an error with matplotlib raise your hand I will help you.

# # 2) One-liner wrapper:
plot_weekly_player_stats(2024, "WR", stat="receiving_yards", top_n=15, week=[1,2,3], save_path="wr_rec_yards_wk1-3.png")

# Use the new plot_player_stat() and plot_weekly_player_stats() to 
# visualize the data into bar graphs and answer the following questions.

# 1. Use each helper function to find your own metric to visualize. 
# Use the weeklyPlayerStats function to find positions and stat columns by name.
# please write in a string which position and metric/ stat you used. The graph
# should be in you files

# example
"I create a graph showing highest interceptions by a qb in 2020"

# 2. Find the player with the most touchdowns in 2024?
# look for WR, and RBs and calculate their rushing and passing TD stat/metric.
"Derick Henry had the highest total touchdowns at 21 TDs"

# 3. Find the player with the highest total passing yards in 2024.

# 4. Which player had the highest rushing yards in week 1 and in week 17?

# Full season stats for Jalen Hurts in 2024 (QB), fuzzy match
#hurts_2024 = get_player_stats_by_name(2024, "Hurts", "QB")

# Exact name match
hurts_2024_exact = get_player_stats_by_name(2024, "J.Hurts", "QB", exact=True)
print(hurts_2024_exact)
# Specific week (e.g., Week 3 only)
hurts_week3 = get_player_stats_by_name(2024, "J.Hurts", "QB", week=3)
#print(hurts_week3)
