from database_utils import DatabaseUtils
from validation_utils import interfaceValidation
from person import users
from passlib.hash import sha256_crypt
from faceRecognise import FaceRecognition


class Menu:
    def __init__(self):
        self.validtionObj=interfaceValidation()
        self.userObj=users()
        self.faceRecObj=FaceRecognition()
    
    #main run function
    def main(self):
        with DatabaseUtils() as db:
            db.createUsersTable()
        self.runMenu()
    
    #run menu
    def runMenu(self):
        while(True):
            print()
            print("1. Register new user")
            print("2. Login")
            print("3. Face recognise login")
            print("4. Quit")
            selection = input("Select an option: ")
            print()
            if(selection == "1"):
                self.register()
            elif(selection == "2"):
                self.login()
            elif(selection == "3"):
                self.faceRecognitionLogin()
            elif(selection == "4"):
                print("Goodbye!")
                exit("Exit complete")
            else:
                print("Invalid input - please try again.")

    #to handle face recognition for login
    def faceRecognitionLogin(self):
        username= self.faceRecObj.run()
        if username != "Unknown":
            self.userObj.userLoginByFaceRegonition(username)
            print("Usename {} Login sucessfully.".format(username))
        else:
            print("Lohin fail as {} user.".format(username))

    #handle register on console
    def register(self):
        print("--- New User ---")
        username=self.toHandleInputUsername("new user name")
        password=self.toHashPassword(self.toHandleInputPassword("new user's password"))
        firstname=self.toHandleInputRealname("first name")    
        lastname=self.toHandleInputRealname("last name")
        email=self.toHandleInputEmail()
        #userObj to registe new user
        self.userObj.newUserRegister(username,password,firstname,lastname,email)

    #to handle input username
    def toHandleInputUsername(self,para):
        self.username = input("Enter the {}: (Back to main menu->'-')".format(para))
        #Add back button
        self.backMainMenu(self.username)
        if self.validtionObj.toCheckInputNull("username",
           self.username) == False or self.validtionObj.toCheckInputSpace("username",
           self.username) == False or self.validtionObj.toCheckInputLetterAndNumber("username",
           self.username) == False or self.validtionObj.toCheckInputLetter("username's first character",
           self.username[0]) == False:
            self.toHandleInputUsername(para)
        return self.username
    
    #to handle input password
    def toHandleInputPassword(self,para):
        self.password = input("Enter the {} password (Back to main menu->'-'): ".format(para))
        #Add back button
        self.backMainMenu(self.password)
        if self.validtionObj.toCheckInputNull("password",
           self.password) == False or self.validtionObj.toCheckInputSpace("password",
           self.password) == False:
            self.toHandleInputPassword(para)
        return self.password
    #to handle input realname
    def toHandleInputRealname(self,para):
        self.tempName = input("Enter the new user's {} (Back to main menu->'-'): ".format(para))
        #Add back button
        self.backMainMenu(self.tempName)
        if self.validtionObj.toCheckInputNull(para,
           self.tempName) == False or self.validtionObj.toCheckInputSpace(para,
           self.tempName) == False or self.validtionObj.toCheckInputLetter(para,
           self.tempName) == False:
            self.toHandleInputRealname(para)
        return self.tempName

    #to handle input email
    def toHandleInputEmail(self):
        self.email = input("Enter the new user's email (Back to main menu->'-'): ")
        #Add back button
        self.backMainMenu(self.email)
        if self.validtionObj.toCheckInputNull("Email address",
           self.email) == False or self.validtionObj.toCheckInputSpace("Email address",
           self.email) == False or self.validtionObj.toValidEmail("Email address",
           self.email) == False:
               self.toHandleInputEmail()
        return self.email

    #to secure password by sha256
    def toHashPassword(self, pwd):
        hashedPassword = sha256_crypt.hash(pwd)
        return hashedPassword

    #to back main menu
    def backMainMenu(self,index):
        if(index == "-"):
            self.runMenu()

    #Login
    def login(self):
        print("--- Login ---")
        username=self.toHandleInputUsername("user name")
        password=self.toHandleInputPassword("user's password")
        #//userObj to check login
        self.userObj.userLogin(username,password)

Menu().main()