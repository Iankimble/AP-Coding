import random


grocery= ['apple','water', 10, 10.232, True,[]]
grocery.append('cookies')

# A Class is a special construct for creating objects - it is the 
# blueprint/ machine for making objects

class Insta_Profile:
  def __init__(self, username, email, location, skills):
    self.username= username
    self.email= email
    self.location= location
    self.skills= skills
    self.usernameCharCount = 14

  def sayHello(self):
    print('hello ')

  def checkUsernameCount(self, username):
    for x in username:
      if username.len() > 14:
        print("retry again. Username must be 13 chars or less")
      else:
        self.username= username
        print('user name accepted.')


 # def firstTime_accountCreation(self, usernmae):
 #  checkUsernameCount(self,username)

# Objects are structured peieces of data that can store data and functions
# simultaniously

# Ex. a job application has the same questions but everyones data 
# is going to be different.

Profile_1= Insta_Profile("EmilyTheBoss", 'etbe@gmail.com', 0,['python','javascript'])
Profile_2= Insta_Profile("CoolGuy", "cg@apple.com", 0, 0)

Profile_2.sayHello()

print(Profile_1)
print(Profile_2.username)
