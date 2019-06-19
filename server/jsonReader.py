import json 
from pathlib import Path

class jasonReader(object):
    """
    A class used to represent read json data
    ...
    Attributes
    ----------
    filename : str
        file name of the json file
    Methods
    -------
    checkFileExist()
        Check the exisiting of the file 
    loadFile()
        load the json file     
    """
    def __init__(self, filename):
        """
        Parameters
        ----------
        filename : str
            The name of the json file
        """        
        self.__filename = filename

    def checkFileExist(self):
        """
        Check the exisiting of the file 
        """        
        config = Path(self.__filename)
        if config.is_file():
            return True
        else:
            return False
    
    def loadFile(self):
        """
        load the json file 
        """ 
        try:
            config = open(self.__filename, encoding = "utf-8")
            data = json.load(config)
            config.close()
            return data
        except:
            raise Exception("File loading error!")

 # configuration json file reader
class dbConfigReader(jasonReader):
    """
    A class used to represent read database seting json data
    ...
    Attributes
    ----------
    filename : str
        file name of the json file
    Methods
    -------
    getHost()
        getter function for host address
    getUser()
        getter function for user name
    getPassword()
        getter function for password
    getDatabase()
        getter function for databse name            
    """
    def __init__(self, filename):
        jasonReader.__init__(self, filename)
        """
        Parameters
        ----------
        __host : str
            host address
        __user : str
            user name 
        __password : str
            password
        __database : str
            database name                       
        """         
        self.__host = "" 
        self.__user = ""
        self.__password = ""
        self.__database = ""

        check = jasonReader.checkFileExist(self)
        if check == True:
            data = jasonReader.loadFile(self)
            try:
                self.__host = data['host'] 
                self.__user = data['user']
                self.__password = data['password']
                self.__database = data['database']
            except:
                raise Exception("loading data error!")    
        else:
            raise Exception("File not found!")

    def getHost(self):
        """
        getter function for host address 
        """ 
        return self.__host

    def getUser(self):
        """
        getter function for user name 
        """
        return self.__user

    def getPassword(self):
        """
        getter function for password
        """
        return self.__password  

    def getDatabase(self):
        """
        getter function for password
        """
        return self.__database                 