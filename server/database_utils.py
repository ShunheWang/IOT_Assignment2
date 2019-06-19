from jsonReader import dbConfigReader
import MySQLdb 

class DatabaseUtils(object):
    """
    A class used to handle database operation
    ...
    Methods
    -------
    insertUser(UserName, Name)
        Check the exisiting of the file 
    getUser(UserName)
        load the json file 
    insertBookTransaction(LmsUserID, BookID, BorrowedDate, CalenderLink)  
        insert book transaction      
    updateBookStatus(BookID, status)
        update book status
    updateBookTransaction(BookBorrowedID, status, ReturnedDate)
        update book transaction
    searchBooks(title)
        search books record
    searchBooksAuthur(Author)
        search books record base on authur name 
    searchBooksISBN(ISBN)
        search books record base on isbn
    listBooks()
        list all the books
    getBook(BookID)
        get book base on book id
    getBookISBN(ISBN)
        get book base on ISBN
    listReturnBooks(userID)
        list the available borrowed book that the user got 
    getReturnBook(userID, BookID)
        get the return book base on the book id
    borrowBook(LmsUserID, BookID, BorrowedDate, CalenderLink)
        operation for borrow book
    returnBook(BookBorrowedID, BookID, ReturnedDate)
        operation for return book
    """
    def __init__(self):
        """
        Parameters
        ----------
        __host : str
            host name
        __user : str
            user name
        __password : str
            password
        __database : str
            database name  
        connection : object
            connection object to the google cloud database                                      
        """
        dbc = dbConfigReader("db.json")

        self.__host = dbc.getHost()
        self.__user = dbc.getUser()
        self.__password = dbc.getPassword()
        self.__database = dbc.getDatabase()
        self.connection = MySQLdb.connect(self.__host, self.__user,
                self.__password, self.__database)

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()        

    def insertUser(self, UserName, Name):
        """
        Parameters
        ----------
        UserName : str
            user's login name
        Name : str
            user's name                                    
        """        
        with self.connection.cursor() as cursor:
            cursor.execute("insert into LmsUser (UserName, Name) values (%s, %s)", (UserName, Name))
        self.connection.commit()

        return cursor.rowcount == 1 

    def getUser(self, UserName):
        """
        Parameters
        ----------
        UserName : str
            user's login name                                    
        """        
        with self.connection.cursor() as cursor:
            cursor.execute("select * from LmsUser where UserName=%s", (UserName,))
            return cursor.fetchall()


    def insertBookTransaction(self, LmsUserID, BookID, BorrowedDate, CalenderLink):
        """
        Parameters
        ----------
        LmsUserID : int
            user's record id
        BookID : str
            book record id 
        BorrowedDate : date
            book borrow date
        CalenderLink : str
            calender link html link                                                           
        """        
        status = "borrowed"
        with self.connection.cursor() as cursor:
            cursor.execute("insert into BookBorrowed (LmsUserID, BookID, Status, BorrowedDate, CalenderLink) values (%s, %s, %s, %s, %s)", (LmsUserID, BookID, status, BorrowedDate, CalenderLink))
        self.connection.commit()

        return cursor.rowcount == 1

    def updateBookStatus(self, BookID, status):
        """
        Parameters
        ----------
        BookID : int
            book record id
        status : str
            book status                                    
        """        
        with self.connection.cursor() as cursor:
            cursor.execute("update Books set Status = %s where bookID = %s", (status, BookID))
        self.connection.commit()

        return cursor.rowcount == 1

    def updateBookTransaction(self, BookBorrowedID, status, ReturnedDate):
        """
        Parameters
        ----------
        BookBorrowedID : int
            user's login name
        status : str
            book status     
        ReturnedDate : date
           book return date                                    
        """        
        with self.connection.cursor() as cursor:
            cursor.execute("update BookBorrowed set Status = %s where BookBorrowedID = %s", ("returned", BookBorrowedID))
            cursor.execute("update BookBorrowed set ReturnedDate = %s where BookBorrowedID = %s", (ReturnedDate, BookBorrowedID))
        self.connection.commit()

        return cursor.rowcount == 1

    def searchBooks(self, title):
        """
        Parameters
        ----------
        title : str
            book title                                    
        """        
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Books where LOWER(Title) like (%s)", ("%" + title.lower() + "%",))
            return cursor.fetchall()

    def searchBooksAuthur(self, Author):
        """
        Parameters
        ----------
        Author : str
            book authur name                                     
        """        
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Books where LOWER(Author) like (%s)", ("%" + Author.lower()  + "%",))
            return cursor.fetchall()

    def searchBooksISBN(self, ISBN):
        """
        Parameters
        ----------
        ISBN : str
            book ISBN                                    
        """        
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Books where ISBN=(%s)", (ISBN,))
            return cursor.fetchall()            

    def listBooks(self):        
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Books")
            return cursor.fetchall()   

    def getBook(self, BookID):
        """
        Parameters
        ----------
        BookID : int
            book record id                                   
        """        
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Books where BookID=(%s)", (BookID,))
            return cursor.fetchall()

    def getBookISBN(self, ISBN):
        """
        Parameters
        ----------
        ISBN : str
            book ISBN                                     
        """        
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Books where ISBN=(%s)", (ISBN,))
            return cursor.fetchall()            

    def listReturnBooks(self, userID):
        """
        Parameters
        ----------
        UserName : str
            user's login name
        Name : str
            user's name                                    
        """        
        with self.connection.cursor() as cursor:
            cursor.execute("select B.Title, B.ISBN, A.BorrowedDate from BookBorrowed A, Books B where A.BookID = B.BookID and A.LmsUserID=(%s) and A.status = 'borrowed'", (userID,))
            return cursor.fetchall()             

    def getReturnBook(self, userID, BookID):
        """
        Parameters
        ----------
        userID : int
            user's record id
        BookID : int
            book record id                                   
        """        
        with self.connection.cursor() as cursor:
            cursor.execute("select * from BookBorrowed where LmsUserID=(%s) and BookID=(%s) and status = 'borrowed'", (userID, BookID))
            return cursor.fetchall()          

    def borrowBook(self, LmsUserID, BookID, BorrowedDate, CalenderLink):
        """
        Parameters
        ----------
        LmsUserID : int
            user's record id
        BookID : int
            book record id
        BorrowedDate : date
            borrow book date        
        CalenderLink : str
            calender link html link                                    
        """         
        self.insertBookTransaction(LmsUserID, BookID, BorrowedDate, CalenderLink)
        status = "borrowed"
        self.updateBookStatus(BookID, status)                                   

    def returnBook(self, BookBorrowedID, BookID, ReturnedDate):
        """
        Parameters
        ----------
        BookBorrowedID : id
            user's login name
        BookID : id
            user's name 
        ReturnedDate : date
            return book date                                        
        """            
        status = "returned"
        self.updateBookTransaction(BookBorrowedID, status, ReturnedDate)
        status1 = "available"
        self.updateBookStatus(BookID, status1) 