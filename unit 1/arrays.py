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
    
# Create a function that will organize our list of numbers from
# least to greatest. 
    
unorderList= [ 23, 600, 4, 91, 22, 49]

unorderList.sort(reverse= True)

print(unorderList)

# Organize list from least to greatest WITHOUT       
# using sort()

# Bubble Sort()

# Algorithms -  essentially instructions for programs that are
# measured by efficiency

# Loop() --> the most basic algorithm - essentially repeats some
# instructions. 

def function():
    for i in []:
        print(i)

hypothetical= []
def loopFunctionManual():
# go through each item 1 by 1
# when it doesnt find the item, skip to next
# when it finds it, print
