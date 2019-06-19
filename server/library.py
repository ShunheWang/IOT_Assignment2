from database_utils import DatabaseUtils
from calender import calender

class Library(object):
    """
    A class used to handle library operation
    ...
    Attributes
    ----------
    username : str
        user login name
    name : str
        user's actual name        
    Methods
    -------
    insertUser()
        register user 
    listBooks()
        list all the books
    searchBooks(title)
        searc book base on title
    searchBooksAuthur(Authur)
        search book base on book authur
    searchBooksISBN(ISBN)
        search book base on book ISBN   
    borrowBook(BookID)
        borrow base on ISBN
    returnBook(BookID)  
        return nook base on ISBN
    listReturnBook()  
        list available return book
    """
    def __init__(self, username, name):
        """
        Parameters
        ----------
        __username : str
            user login name
        __name : str
            user's actual name  
        """
        self.__username = username
        self.__name = name

    def insertUser(self):
        print("--- Insert User ---")
        with DatabaseUtils() as db:
            if(db.insertUser(self.__username, self.__name)):
                print("{} inserted successfully.".format(self.__username))
            else:
                print("{} failed to be inserted.".format(self.__username))
       
    def listBooks(self):
        print("--- Book ---")
        print("{:<15} {:<15} {:<15} {:<15} {}".format("Title", "Authur", "Publish Date", "ISBN", "Status"))
        with DatabaseUtils() as db:
            for book in db.listBooks():
                print("{:<15} {:<15} {:<15} {:<15} {}".format(book[1], book[2], book[3].strftime('%Y-%m-%d'), book[5], book[4]))

    def searchBooks(self, title):
        """
        Parameters
        ----------
        title : str
            book title
        """
        print("--- Book ---")
        print("{:<15} {:<15} {:<15} {:<15} {}".format("Title", "Authur", "Publish Date", "ISBN", "Status"))
        with DatabaseUtils() as db:
            for book in db.searchBooks(title):
                print("{:<15} {:<15} {:<15} {:<15} {}".format(book[1], book[2], book[3].strftime('%Y-%m-%d'), book[5], book[4])) 

    def searchBooksAuthur(self, Authur):
        """
        Parameters
        ----------
        Authur : str
            book aurthur name
        """
        print("--- Book ---")
        print("{:<15} {:<15} {:<15} {:<15} {}".format("Title", "Authur", "Publish Date", "ISBN", "Status"))
        with DatabaseUtils() as db:
            for book in db.searchBooksAuthur(Authur):
                print("{:<15} {:<15} {:<15} {:<15} {}".format(book[1], book[2], book[3].strftime('%Y-%m-%d'), book[5], book[4])) 

    def searchBooksISBN(self, ISBN):
        """
        Parameters
        ----------
        BookID : str
            book ISBN
        """
        print("--- Book ---")
        print("{:<15} {:<15} {:<15} {:<15} {}".format("Title", "Authur", "Publish Date", "ISBN", "Status"))
        with DatabaseUtils() as db:
            for book in db.searchBooksISBN(ISBN):
                print("{:<15} {:<15} {:<15} {:<15} {}".format(book[1], book[2], book[3].strftime('%Y-%m-%d'), book[5], book[4]))


    def borrowBook(self, BookID):
        """
        Parameters
        ----------
        BookID : str
            book ISBN
        """
        with DatabaseUtils() as db:
            userId = 0
            for user in db.getUser(self.__username):
                userId = user[0]
        
            if (userId == 0):
                self.insertUser()
                for user in db.listBooks():
                    userId = user[0]

            gotBook = False
            status = ""
            title = ""
            id = 0

            for book in db.getBookISBN(BookID):
                gotBook = True
                status = book[4]
                title = book[1]
                id = book[0]

            if (gotBook == False):
                print("no book record found!")
            else: 
                if (status == "borrowed"):
                   print("the book is not available for borrow!")
                else:
                    cal = calender()
                    bDate = cal.getBorrowedDate()
                    cLink = cal.insertCalender(self.__username, title)
                    print(id)
                    db.borrowBook(userId, id, bDate, cLink)

    def returnBook(self, BookID):
        """
        Parameters
        ----------
        BookID : str
            book ISBN
        """
        with DatabaseUtils() as db:
            userId = 0
            for user in db.getUser(self.__username):
                userId = user[0]

            if (userId == 0):
                self.insertUser()
                for user in db.listBooks():
                    userId = user[0]  

            id = 0 
            gotBook = False       

            for book in db.getBookISBN(BookID):
                gotBook = True
                id = book[0] 

            if (gotBook == False):
                print("no book record found!")
            else:
                BookBorrowedID = 0

                for book in db.getReturnBook(userId, id):
                    BookBorrowedID = book[0]
                    cLink = book[6]

                if (BookBorrowedID == 0):
                    print("no borrow book found!")
                else: 
                    cal = calender()
                    
                    rDate = cal.getReturnDate()

                    cal.removeEvent(cLink)

                    db.returnBook(BookBorrowedID, id, rDate)

    def listReturnBook(self):
       with DatabaseUtils() as db:
            userId = 0
            for user in db.getUser(self.__username):
                userId = user[0]                 
            
            if (userId == 0):
                self.insertUser()
                for user in db.listBooks():
                    userId = user[0]

            print("{:<15} {:<15} {:<15}".format("Title", "ISBN", "Borrowed Date"))
            for book in db.listReturnBooks(userId):
                print("{:<15} {:<15} {:<15}".format(book[0], book[1], book[2].strftime('%Y-%m-%d')))                             