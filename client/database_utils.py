import sqlite3

class DatabaseUtils:
    """
    A class used to handle database operation
    ...
    Methods
    -------
    createConnection()
        create database connection
    createUsersTable()
        create user table
    insertNewUser(newData)  
        insert new user      
    searchUserPassword(userData)
        search user password
    searchUserData(userData)
        search user data
    """    
    def __init__(self, connection = None):
        """
        Parameters
        ----------
        connection : object
            database connection                                      
        """        
        if(connection == None):
            connection = self.createConnection()
        self.connection = connection

    def __enter__(self):
        return self

    def close(self):
        self.connection.close()

    def __exit__(self, type, value, traceback):
        self.close()
    
    def createConnection(self):
        try:
            conn = sqlite3.connect('iot_assignment2.db')
            return conn
        except:
            raise Exception("Database connection error!")

    #create table
    def createUsersTable(self):
        conn=self.createConnection()
        cur=conn.cursor()
        try:
            cur.execute('CREATE TABLE if not exists Users(username CHAR(20) PRIMARY KEY NOT NULL,'
                                                         'password CHAR(50) NOT NULL,'
                                                         'firstname CHAR(10) NOT NULL,'
                                                         'lastname CHAR(10) NOT NULL,'
                                                         'email CHAR(25) NOT NULL)')
            conn.commit()
            conn.close()
        except:
            conn.close()
            raise Exception("Create users table fail!")

    #insert new user for register
    def insertNewUser(self,newData):
        """
        Parameters
        ----------
        newData : tupple
            user information                                      
        """        
        conn=self.createConnection()
        cur=conn.cursor()
        try:
            cur.execute("insert into Users(username, password, firstname, lastname, email) values (?, ?, ?, ?, ?)", (newData))
            conn.commit()
            conn.close()
            return True
        except:
            conn.close()
            return False

    #search user password by name
    def searchUserPassword(self,userData):
        """
        Parameters
        ----------
        userData : str
            user namee                                      
        """        
        conn=self.createConnection()
        cur=conn.cursor()
        try:
            cur.execute("select password from Users where username=?", (userData,))
            row = cur.fetchone()
            conn.commit()
            conn.close()
            return row
        except:
            conn.close()
            raise Exception("Search table fail!")

    #serarch user data by name
    def searchUserData(self,userData):
        """
        Parameters
        ----------
        userData : str
            user name                                     
        """        
        conn=self.createConnection()
        cur=conn.cursor()
        try:
            cur.execute("select username,firstname,lastname from Users where username=?", (userData,))
            row = cur.fetchone()
            conn.commit()
            conn.close()
            return row
        except:
            conn.close()
            raise Exception("Get user data fail!")