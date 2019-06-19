from library import Library
from voice_utils import voiceInput
from scan_utils import barcodeScan

class libraryMenu(object):
    """
    A class used to handle library menu
    ...
    Attributes
    ----------
    username : str
        user login name
    name : str
        user's actual name 
    Methods
    -------
    runMenu()
        run the menu    
    """
    def __init__(self, username, name):
        self.library = Library(username, name)
        self.__username = username
        self.__name = name

    # check json file
    def runMenu(self):
        while(True):
            print()
            print("1. list all the books")
            print("2. search  Book by title")
            print("3. search  Book by authur name")
            print("4. search  Book by ISBN")
            print("5. search  Book by voice")
            print("6. Borrow")
            print("7. Return")
            print("8. Logout")
            print() 
            selection = input("Select an option: ")
            print() 

            if selection == "1":
                self.library.listBooks()
            elif selection == "2":
                title = input("Enter the Book Title:")
                self.library.searchBooks(title)
            elif selection == "3":
                aName = input("Enter the Authur Name:")
                self.library.searchBooksAuthur(aName)
            elif selection == "4":
                isbn = input("Enter the ISBN:")
                self.library.searchBooksISBN(isbn)
            elif selection == "5":
                voiceResult = voiceInput() 
                title = voiceResult.run()
                self.library.searchBooks(title)                                
            elif selection == "6":
                while(True):
                    print()
                    print("1. Normal mode Borrow Book")
                    print("2. Voice mode Borrow Book")
                    print("3. Back")
                    print()
                    selection1 = input("Select an option: ")
                    print()

                    if selection1 == "1":
                        id = input("Enter the Borrowing Book ISBN Code:")
                        self.library.borrowBook(id)
                        break
                    elif selection1 == "2":
                        voiceResult = voiceInput() 
                        title = voiceResult.run()
                        self.library.searchBooks(title)
                        
                        id = input("Enter the Borrowing Book ISBN Code:")
                        self.library.borrowBook(id)
                        break
                    elif selection1 == "3":
                        break
                    else:
                        print("Invalid input - please try again.")    
            elif selection == "7":
                self.library.listReturnBook()
                print()
                
                while(True):
                    print()
                    print("1. Normal mode Borrow Book")
                    print("2. Scan mode Borrow Book")
                    print("3. Back")
                    print()
                    selection1 = input("Select an option: ")
                    print()

                    if selection1 == "1":
                        id = input("Enter the returning Book ISBN Code:")
                        self.library.returnBook(id)
                        break
                    elif selection1 == "2":
                        scan = barcodeScan()
                        
                        id = scan.run()
                        self.library.returnBook(id)
                        break
                    elif selection1 == "3":
                        break    
                    else:
                        print("Invalid input - please try again.")                                
            elif selection == "8":
                print("Exit the program.......")
                print() 
                break
            else:
                print("Invalid input - please try again.")                      