# Activity: 
# Create a function that will LOOP through 
# and print each number in the list and stops at the 48. 
# In your function, the list and the value 
# that needs to be found should be passed as arguments. 

numbersList = [ 1,20,39,48,72,83]
value = 48

def numberThing(numberList, value):
    for x in numberList:
        print(x)
        if x == value:
            break
        
numberThing(numbersList,value)
    