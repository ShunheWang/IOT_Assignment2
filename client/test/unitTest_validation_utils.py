import unittest
import sys
sys.path.append('..')
from validation_utils import interfaceValidation

class Test_InterfaceValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("interfaceValidation test start")

    def setUp(self):
        print("init interfaceValidation class object")
        print("----------------------------------------------------")
        self.ifvObj=interfaceValidation()

    def test_toCheckInputNull(self):
        trueOne = self.ifvObj.toCheckInputNull("something","abc123")
        falseOne = self.ifvObj.toCheckInputNull("something","")
        self.assertTrue(trueOne)
        self.assertFalse(falseOne)

    def test_toCheckInputSpace(self):
        trueOne = self.ifvObj.toCheckInputSpace("something"," abc 123 ")
        falseOne = self.ifvObj.toCheckInputSpace("something"," ")
        self.assertTrue(trueOne)
        self.assertFalse(falseOne)
    
    def test_toCheckInputLetterAndNumber(self):
        trueOne = self.ifvObj.toCheckInputLetterAndNumber("something","abc123")
        falseOne = self.ifvObj.toCheckInputLetterAndNumber("something","abc123-=!")
        self.assertTrue(trueOne)
        self.assertFalse(falseOne)

    def test_toCheckInputLetter(self):
        trueOne = self.ifvObj.toCheckInputLetter("something","abc")
        falseOne = self.ifvObj.toCheckInputLetter("something","abc123")
        self.assertTrue(trueOne)
        self.assertFalse(falseOne)

    def test_toValidEmail(self):
        trueOne = self.ifvObj.toValidEmail("something","abc@gmail.com")
        falseOne = self.ifvObj.toValidEmail("something","abc")
        falseTwo = self.ifvObj.toValidEmail("something","abc@abc")
        self.assertTrue(trueOne)
        self.assertFalse(falseOne)
        self.assertFalse(falseTwo)

    def tearDown(self):
        print("----------------------------------------------------")

    @classmethod
    def tearDownClass(cls):
        print("interfaceValidation test finish")

if __name__ == '__main__':
    unittest.main()