import pandas as pd
import nfl_data_py as nfl
import matplotlib.pyplot as plt
import pandas as pd


from helperFunctions import get_team_records, get_season_Results_By_team, weeklyPlayerStats

# schedules = get_team_records(2025)
# print(schedules)

# My hypothesis - The best point differentials are probably
# going to be the best teams.

top6_Teams = ['TB','IND','LA','BUF','SF','SEA']

# find the point differential for each team listed
# formula for PD = points for - points against

team_1 = get_season_Results_By_team(2025,'TB') # 14 PD
team_2= get_season_Results_By_team(2025,'IND') # 78 PD
team_3= get_season_Results_By_team(2025,'LA')
team_4= get_season_Results_By_team(2025,'BUF') # 7~ PD
team_5= get_season_Results_By_team(2025, 'SF') # -8 PD
team_6= get_season_Results_By_team(2025, 'SEA')

#print(team_1)
# print(team_2)
# print(team_3)
# print(team_4)
# print(team_5)
print(team_6)

# 1. Which team has the best point differential this season ?
'The best overall PD is INDY. They have a point differiential of 78 pts'

# 2. Which team has the worst point differential this season ?
'The worst overall PD is SF. They have a point differiential of -3 pts.'

# 3. Which team has the best home point differential this season ?
'The best home PD is...'

# 4. Which team has the best away point differential this season ? 
'The best away PD is...'


# In your exercise2.py document, create a function that will 
# allow you to enter different numbers individually and 
# calculate the sum of those numbers. Your function should operate 
# on a while loop and allow the user to enter each number 
# 1 at a time, as many times as they want. Your function 
# should ask the user if they are done entering numbers,  
# When the user is done entering numbers your function 
# should add up and return the sum of those numbers. 
# If they are not done entering in numbers it should allow 
# them to enter another one.

def pdCheck():
    print("Please enter a number")
    number = input()
    values = []
    
    while number != 'q':
        values.append(int(number))
        print(values)
        print("Please enter a number")
        number = input()          
    else:
        print('doing caluclation...') 
        total = sum(values)
        print(total)

# 3. Which team has the best home point differential this season ?
'The best home PD is...INDY 64' 

# 4. Which team has the best away point differential this season ? 
'The best away PD is...SEA 19'
 
pdCheck()


