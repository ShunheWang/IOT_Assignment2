from database_utils import DatabaseUtils
from passlib.hash import sha256_crypt
from socketClient import socketClient

class users:
    """
    A class used to handle user login process
    ...
    Methods
    -------
    newUserRegister(username,password,firstname,lastname,email):
        register new user
    userLoginByFaceRegonition(username):
        facial regonition login
    userLogin(username,password):
        normal user login                
    """    
    def newUserRegister(self,username,password,firstname,lastname,email):
        """
        Parameters
        ----------
        username : str
           user name
        password : str
            password
        firstname : str
            user first name
        lastname : str
            user last name
        email : str
            email                                                                                      
        """        
        with DatabaseUtils() as db:
            #put all data into a tuple
            inputData = (username, password, firstname, lastname, email)
            #check insert data suceess or fail
            if(db.insertNewUser(inputData)==True):
                print("Username is {} ,Data inserted successfully.".format(username))
            else:
                print("Data failed to be inserted coz {} exist.".format(username))

    def userLoginByFaceRegonition(self,username):
        """
        Parameters
        ----------
        username : str
           user name                                                                                      
        """        
        with DatabaseUtils() as db:
            inputData = (username)
            #then call Jun function to connect with another rasp pi
            loginUserData=db.searchUserData(inputData)
            userName=loginUserData[0]
            realName=loginUserData[1]+" "+loginUserData[2]
            print("userName: ",userName)
            print("realName: ",realName)
            socketClient(userName,realName).mainRun()

    def userLogin(self,username,password):
        """
        Parameters
        ----------
        username : str
           user name
        password : str
            password                                                                                      
        """        
        with DatabaseUtils() as db:
            inputData = (username)
            hashedPassword=db.searchUserPassword(inputData)
            if(hashedPassword !=None):
                #check password
                hashPassword=hashedPassword[0]
                if(sha256_crypt.verify(password, hashPassword)):
                    print("Usename {} Login sucessfully.".format(username))
                    #then call Jun function to connect with another rasp pi
                    loginUserData=db.searchUserData(inputData)
                    userName=loginUserData[0]
                    realName=loginUserData[1]+" "+loginUserData[2]
                    socketClient(userName,realName).mainRun()
                else:
                    print("Usename {} password incorrect, Login fail".format(username))
            else:
                print("Login fail coz usename {} is not exist.".format(username))
