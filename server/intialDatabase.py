import MySQLdb

class DatabaseUtils:
    HOST = "35.197.171.6"
    USER = "root"
    PASSWORD = "root"
    DATABASE = "People"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(DatabaseUtils.HOST, DatabaseUtils.USER,
                DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def getPeople(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select PersonID, Name from Person")
            return cursor.fetchall()    

    def createUserTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table LmsUser (
	                LmsUserID int not null auto_increment,
                    UserName nvarchar(256) not null,
                    Name text not null,
                    constraint PK_LmsUser primary key (LmsUserID),
                    constraint UN_UserName unique (UserName)
                )""")
        self.connection.commit()

    def createBookTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table Books (
	                BookID int not null auto_increment,
                    Title text not null,
                    Author text not null,
                    PublishedDate date not null,
                    Status enum ('available', 'borrowed'),
                    ISBN text not null,
                    SequenceNo int not null,
                    constraint PK_Book primary key (BookID) 
                )""")
        self.connection.commit()

    def createBookBorroweedTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table BookBorrowed (
                    BookBorrowedID int not null auto_increment,
                    LmsUserID int not null,
                    BookID int not null,
                    Status enum ('borrowed', 'returned'),
                    BorrowedDate date not null,
                    ReturnedDate date null,
                    CalenderLink text not null,
                    constraint PK_BookBorrowed primary key (BookBorrowedID)
                )""")
        self.connection.commit()

    def insertBook(self):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into Books (Title, Author, PublishedDate, Status, ISBN, SequenceNo) values (%s, %s, %s, %s, %s, %s)", ("Harry Potter", "Gavin", "2019-1-12", "available", "1234-1", 1))
            cursor.execute("insert into Books (Title, Author, PublishedDate, Status, ISBN, SequenceNo) values (%s, %s, %s, %s, %s, %s)", ("Lion King", "Gavin", "2019-2-12", "available", "1235-1", 1))
            cursor.execute("insert into Books (Title, Author, PublishedDate, Status, ISBN, SequenceNo) values (%s, %s, %s, %s, %s, %s)", ("Three Kingdom", "Steven", "2019-3-12", "available", "1267-1", 1))
            cursor.execute("insert into Books (Title, Author, PublishedDate, Status, ISBN, SequenceNo) values (%s, %s, %s, %s, %s, %s)", ("Advance Maths", "Leo", "2019-1-12", "available", "1345-1", 1))
        self.connection.commit()

    def getUser(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select LmsUserID, UserName, Name from LmsUser")
            return cursor.fetchall()        

    def getTransaction(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select BookBorrowedID, LmsUserID, BookID, Status, BorrowedDate, ReturnedDate, CalenderLink from BookBorrowed")
            return cursor.fetchall()


#with DatabaseUtils() as db:  
#    for person in db.getPeople():
#        print("{:<15} {}".format(person[0], person[1]))      

#with DatabaseUtils() as db:  
#    db.insertBook()
    #db.createBookTable()
    #db.createBookBorroweedTable()