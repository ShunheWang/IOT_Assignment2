import unittest
import sys
sys.path.append('..')
from socketClient import socketClient

class Test_socketClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("socketClient test start")

    def setUp(self):
        print("init socketClient class object")
        print("----------------------------------------------------")
        self.slObj=socketClient("username","realname")
    
    def test_generateJsonData(self):
        trueOne = self.slObj.generateJsonData("maison","shunhewang")
        falseOne = self.slObj.generateJsonData("maison","shunhewang")
        trueOneTestData={"username": "maison", "realName": "shunhewang"}
        falseOneTestData={"username": "maison1", "realName": "shunhewang1"}
        self.assertEqual(trueOne,trueOneTestData)
        self.assertNotEqual(falseOne,falseOneTestData)
    
    def tearDown(self):
        print("----------------------------------------------------")
    
    @classmethod
    def tearDownClass(cls):
        print("socketClient test finish")

if __name__ == '__main__':
    unittest.main()