# Create a function that will return the largest 
# and smallest numberin an array
numbers =[ 0 , 1, 5, 10, 20, 39, 48, 83, 89, 72, 90,10202, 1292 ] 
# min / max

def minMax():
    x = min(numbers)
    y = max(numbers)

    print(x , y)

#minMax()

# Create a function that will reverse the characters in a string.
# your string must be passed into the function as a parameter
# EXAMPLE: book = koob 
# car = rac

def reverseString(word):
    text = word[::-1]
    print(text)  

    newWord = list(word)
    print(newWord.reverse())
    print(newWord)

reverseString('anything')