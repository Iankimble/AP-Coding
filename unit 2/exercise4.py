from helperFunctions import weeklyPlayerStats, plot_player_stat, plot_weekly_player_stats, get_position_columns
import matplotlib.pyplot as plt

stats = weeklyPlayerStats(2024, "WR")  
print(stats)
plot_player_stat(stats, stat="rushing_tds", top_n=10, title="WR rushing TDs (2024)", save_path="WR_rushing_tds_2024.png"  )

# You can copy and paste this code from the AP repo. the document is called exercise4.py
# in the unit2 folder. 

# Try to run the code above.

# If you have an error with matplotlib raise your hand I will help you.

# 2) One-liner wrapper:
plot_weekly_player_stats(2024, "WR", stat="receiving_yards", top_n=15, week=[1,2,3], save_path="wr_rec_yards_wk1-3.png")


# Use the new plot_player_stat() and plot_weekly_player_stats() to visualize the data into bar graphs and answer the following questions.

# 1. Use each helper function to find your own metric to visualize. use the weeklyPlayerStats function to find positions and stat columns by name
 
# 2. Find the player with the most touchdowns in 2024?

# 3. find the player with the highest total passing yards in 2024.

# 4. which player had the highest rushing yards in week 1 and in week 17?