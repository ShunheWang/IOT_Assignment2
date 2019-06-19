import re

class interfaceValidation:
    """
    A class used to handle input validation
    ...
    Methods
    -------
    toCheckInputNull(checkInfo,checkValue)
        check empty value 
    toCheckInputSpace(checkInfo,checkValue)
        check spacing
    toCheckInputLetterAndNumber(checkInfo,checkValue) 
        letter and number format validation      
    toCheckInputLetter(checkInfo,checkValue)
        letter format validation
    toValidEmail(checkInfo,checkValue)
        email format validation
    """
    #check input is null
    def toCheckInputNull(self,checkInfo,checkValue):
        """
        Parameters
        ----------
        checkInfo : str
           msg message
        checkValue : int
            checkData checkData                                                                                    
        """  
        if len(checkValue) == 0:
            print("Input {} cannot be null.".format(checkInfo))
            return False
        return True

    #check input is space
    def toCheckInputSpace(self,checkInfo,checkValue):
        """
        Parameters
        ----------
        checkInfo : str
           msg message
        checkValue : int
            checkData checkData                                                                                    
        """  
        if checkValue.isspace() == True:
            print("Input {} cannot be only space.".format(checkInfo))
            return False
        return True

    #check input is letter and number
    def toCheckInputLetterAndNumber(self,checkInfo,checkValue):
        """
        Parameters
        ----------
        checkInfo : str
           msg message
        checkValue : int
            checkData checkData                                                                                    
        """  
        if checkValue.isalnum() == False:
            print("Input {} can be only letter or number.".format(checkInfo))
            return False
        return True

    #check input is letter
    def toCheckInputLetter(self,checkInfo,checkValue):
        """
        Parameters
        ----------
        checkInfo : str
           msg message
        checkValue : int
            checkData checkData                                                                                    
        """
        if checkValue.isalpha() == False:
            print("{} can be only letter.".format(checkInfo))
            return False
        return True

    #check email format 
    def toValidEmail(self,checkInfo,checkValue):
        """
        Parameters
        ----------
        checkInfo : str
           msg message
        checkValue : int
            checkData checkData                                                                                    
        """
        reEmail = re.compile(r'^[a-zA-Z\.]+@[gmail|outlook|126|foxmail]+\.[a-zA-Z]{3}$')
        if reEmail.match(checkValue) == None:
            print("{} format is invalid.".format(checkInfo))
            return False
        return True 