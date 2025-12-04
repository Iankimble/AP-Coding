from helperFunctions import get_season_totals_by_position, plot_position_stat_bar, plot_player_stat_by_week, get_player_stats

# rb for '24
#plot_position_stat_bar(2024,'RB',"rushing_yards",save_path='rb rushing yards 2024')
#  rb for '23
#plot_position_stat_bar(2023,'RB',"rushing_yards",save_path='rb rushing yards 2023')
# rb for '22
#plot_position_stat_bar(2022,'RB',"rushing_yards",save_path='rb rushing yards 2022')

bestRb24= get_season_totals_by_position(2024, 'RB')
bestRb23= get_season_totals_by_position(2023, 'RB')
bestRb22= get_season_totals_by_position(2022, 'RB')

#print(bestRb22)
#print(bestRb23)
#print(bestRb24)

answer=  'derick henry has the most rushing yards over the course of 2022-2024'

#plot_player_stat_by_week(2024, 'Jalen','Hurts',"passing_yards", save_path='Jalen Hurts Passing Yards 2024')
#plot_player_stat_by_week(2023, 'Jalen','Hurts',"passing_yards", save_path='Jalen Hurts Passing Yards 2023')
#plot_player_stat_by_week(2022, 'Jalen','Hurts',"passing_yards", save_path='Jalen Hurts Passing Yards 2022')

Jalen24 = get_player_stats(2024,'Jalen','Hurts')
# print(Jalen24)
qbNumbers= get_season_totals_by_position(2024,'QB')
print(qbNumbers)