# Objects are construct for storing data and functions together
# when creating an object we start with the class keyword.
# This acts like our object maker/ our blueprint.

class CarMaker:
    def __init__(self, name, color, seating, year, model, miles): # initializes the blueprint 
        self.name = name
        self.color = color
        self.seating = seating
        self.year = year
        self.model = model
        self.miles =  miles

    def printInfo(self):
        print('heres your car FAQS') # FACT
        print('name: ' + self.name)
        print('year: ' + str(self.year))
        print('miles: ' + str(self.miles))

    def windshieldwippers(self):
        print("when raining turn on")
        
    def airbag(self):
        print("when driving a certain speed anc a collision happens; open")

    def turnsignals(self, up, down):
        if up == 1:
            print("turn left")
        elif down == 2:
            print("turn right")
        else:
            print("dont turn signals on")
        
    def bluetooth(self, year):
        if year > 2020:
            print("you have bluetooth")
        else:
            print("no bluetooth on this model")

carOption1 = CarMaker('carolla', 'black','2', '2024','carolla', 20000) # creating actual car data.
print(carOption1) # shows the location in computer memory
carOption1.printInfo() # shows me actual data













class instaProfile:
    def __init__(self, username, email, profileImg, pw, bio):
        self.username = username
        self.email = email
        self.profileImg = profileImg
        self.pw = pw
        self.bio = bio

    def printInfo(self):
        print('username ' + self.username,)
        print('email: '+ self.email)

    def resetPw(self):
        print('2-step auth...')

    def uploadPicture(self):
        print('instructions')

    def viewFollowers(self):
        print(['list of other followers'])

profile1 = instaProfile('Ian','ik@aoil.com','pic.png','123','lorem ipsum')
profile2 = instaProfile('Rob','rob@gmail.com','pic.png','321','lorem ipsum')

# profile1.printInfo()
# profile2.printInfo()


#class Phone:
 #   def __init__(self,name):
  #      self.name = name
        # create 3 more attributes

   # def example():
        # create 3 functions that phones use

#phoneA = Phone()

#phoneB = Phone()

# print the data from phoneA and phoneB and also run a function from both 
# phoneA and B.
