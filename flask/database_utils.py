import MySQLdb
"""
connect to cloud database 
ceate the table 
insert the database

"""
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

    def createBooksTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists Books")
            cursor.execute("""
                create table if not exists Books (
                    ISBN int not null auto_increment,
                    AuthorName text ,
                    BookName text ,
                    number int ,
                    constraint PK_Books primary key (ISBN)
                )""")
            cursor.execute("insert into Books (AuthorName, BookName, number) values (%s, %s, %s)", ("Gavin", "HarryPot", 3))
            cursor.execute("insert into Books (AuthorName, BookName, number) values (%s, %s, %s)", ("Gavin", "LionKing", 5))
            cursor.execute("insert into Books (AuthorName, BookName, number) values (%s, %s, %s)", ("Steven", "three body", 2))
            cursor.execute("insert into Books (AuthorName, BookName, number) values (%s, %s, %s)", ("Lion", "mathmatic", 1))
        self.connection.commit()

    def insertBook(self, ISBN,AuthorName,BookName,Avaliable):
        with self.connection.cursor() as cursor:
             cursor.execute("insert into Books (AuthorName, BookName, Avaliable) values (%s, %s, %s)", (AuthorName, BookName, Avaliable))
        self.connection.commit()

        return cursor.rowcount == 1

    def getBook(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Books")
            return cursor.fetchall()
    def searchBookISBN(self, ISBN):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Books where ISBN=(%s)", (ISBN,))
            return cursor.fetchall()
    def searchBookAuthorName(self, AuthorName):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Books where AuthorName=(%s)", (AuthorName,))
            return cursor.fetchall()
    def searchBookBookName(self, BookName):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Books where BookName=(%s)", (BookName,))
            return cursor.fetchall()


    def deletePerson(self, ISBN):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from Books where ISBN != %s", (ISBN,))
        self.connection.commit()

# function get the sequnece number
    def getBookSequence(self,Title):
        with self.connection.cursor() as cursor:
            cursor.execute("select distinct max(SequenceNo) from Books where LOWER(Title)=(%s)",(Title.lower(),))
            return cursor.fetchall()
#get state of book 
    def getBookState(self,Bookid):
        with self.connection.cursor() as cursor:
            cursor.execute("select Status from Books where Bookid=(%s)",(Bookid.lower(),))
            return cursor.fetchall()
#get the number of book id 
    def getBookborrow(self,Bookid):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(BookBorrowID) from BookBorrowed where BookID=(%s)",(Bookid,))
            return cursor.fetchall()
# get the all the title in the books
    def getTitle(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select Title from Books ")
            return cursor.fetchall()

      #cursor.execute("select State from Books where LOWER(Title)=(%s)",("%"+Title.lower()+"%",))      