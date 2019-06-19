# Reference: https://docs.python.org/2/library/unittest.html
import unittest
import sqlite3
import sys
sys.path.append('..')
from database_utils import DatabaseUtils

class Test_databaseUtils(unittest.TestCase):

    def setUp(self):
        self.db=DatabaseUtils()    
        self.db.createUsersTable()

    def dataCount(self):
        conn=self.db.createConnection()
        cur=conn.cursor()
        try:
            cur.execute("select count(*) from Users")
            row = cur.fetchone()
            conn.commit()
            conn.close()
            return row[0]
        except:
            conn.close()
            raise Exception("Search data counts fail!")
        
    def test_insertNewUser(self):
        trueData=("username", "password", "firstname", "lastname", "email")
        self.assertEqual(self.dataCount(),0)
        trueOne = self.db.insertNewUser(trueData)
        self.assertTrue(trueOne)
        self.assertEqual(self.dataCount(),1)
        
        falseData="anything"
        falseOne = self.db.insertNewUser(falseData)
        self.assertFalse(falseOne)
        self.assertNotEqual(self.dataCount(),2)

    def test_searchUserPassword(self):
        trueData=("username")
        password = self.db.searchUserPassword(trueData)
        if(password[0]!=None):
            if(password[0]=="password"):
                print("Test passed")
            else:
                print("Test Failed")
        else:
            print("Test Failed")

        wrongData=("username1")
        anotherPassword = self.db.searchUserPassword(wrongData)
        if(anotherPassword!=None):
            print("Test failed")
        else:
            print("Test passed")

    def test_searchUserData(self):
        matchData=("username", "firstname", "lastname")
        trueData=("username")
        userData = self.db.searchUserData(trueData)
        self.assertEqual(userData,matchData)
        
        trueData=("username1")
        userData = self.db.searchUserData(trueData)
        self.assertNotEqual(userData,matchData)

if __name__ == "__main__":
    unittest.main()