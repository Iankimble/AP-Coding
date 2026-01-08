def doMath():
    result = 2 * 2
    # print(result) 
    return(result) # 4 is stuck here

#doMath()

def addMath():
    val = doMath() # this function returns 4
    newRsult = val + 2 # 4+ 2
    print(newRsult)

addMath()