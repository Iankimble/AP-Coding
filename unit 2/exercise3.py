
# Copy the new weeklyPlayerStats() function into your helperFunction.py file.

# Create a new python document caled  exercise3.py . Using th individual player helper function, 
# answer the following questions:

# NOTE = you will need to pass the position, year and week in as an agrument
# position example:
  
# - quarterback = 'QB'
# - runnerback = 'RB'
# - wide receiver = 'WR'

from helperFunctions import weeklyPlayerStats

exampleData = weeklyPlayerStats(2024,'WR') 
# (Year, Position, Week of season)
# The week argument is optional, if you remove the weeek it will give the entire season data.

print(exampleData)

# NOTE = Please write your responses in string format 
'Please write your responses in string format'

# 1. Who are the top 5 quarterbacks by passing yards in 2024? 
# What was their average completion percentage (cmp_pct)?

# 2. What does a high cmp_pct (completion percentage) tell you about a
# quarterback’s style of play?
 
# 3. Which RB had the highest rushing yards in 2024? 
# Which RB had the best yards per carry (rush_ypc) in 2024? Are these the same or different individuals?
'Rushing yards - S.Barkley '
'Yards per carry - D.Henry '

# 4. If a RB has high rushing yard (rush_yards), but low rushing yards per carry (rush_ypc),
#  what could that mean?

# 5. Find a player who has the best recieving yards on the fewest pass attempts?
# for example they have alot of yards after catching the ball but they dont get many targets

'L.McConkey'