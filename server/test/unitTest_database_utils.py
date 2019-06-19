# Reference: https://docs.python.org/2/library/unittest.html
import unittest
import sys
sys.path.append('..')
from database_utils import DatabaseUtils

class Test_DatabaseUtils(unittest.TestCase):
    def setUp(self):
        self.db=DatabaseUtils()
    
    def dataCount(self):
        with self.db.connection.cursor() as cursor:
            cursor.execute("select count(*) from LmsUser")
            return cursor.fetchone()[0]

    def test_getUser(self):
        count = self.dataCount()
        try:
            trueResult=self.db.getUser("username")
            print("Test passed")
        except:
            print("Test failed")

    def test_insertBookTransaction(self):
        testData=(1,1,"2019-01-01","abc")
        result=self.db.insertBookTransaction(testData[0],testData[1],testData[2],testData[3])
        print("result: ",result)
        self.assertTrue(result)

    def test_updateBookStatus(self):
        testData=(1,"anything")
        result=self.db.updateBookStatus(testData[1],testData[0])
        self.assertFalse(result)

    def test_updateBookTransaction(self):
        testData=(1,"anything","2019-01-01")
        result=self.db.updateBookTransaction(testData[0],testData[1],testData[2])
        self.assertFalse(result)
    
    def test_searchBooks(self):
        result=self.db.searchBooks("abc")
        self.assertFalse(result)
        result=self.db.searchBooks("Harry")
        self.assertTrue(result)
    
    def test_searchBooksAuthur(self):
        result=self.db.searchBooksAuthur("abc")
        self.assertFalse(result)
        result=self.db.searchBooksAuthur("gavin")
        self.assertTrue(result)
    
    def test_searchBooksISBN(self):
        result=self.db.searchBooksISBN(1)
        self.assertFalse(result)

    def test_listBooks(self):
        result=self.db.listBooks()
        self.assertTrue(result)

    def test_getBook(self):
        result=self.db.getBook(1)
        self.assertTrue(result)

    def test_getBookISBN(self):
        result=self.db.getBookISBN(1)
        self.assertFalse(result)

    def test_listReturnBooks(self):
        result=self.db.listReturnBooks(1)
        self.assertTrue(result)

    def test_getReturnBook(self):
        result=self.db.getReturnBook(1,1)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()