# Reference: reference the source code from tutorial provide from RMIT 
import socket, json, sys
from menu import libraryMenu
import socket_utils

class server:
    """
    A class used to work as socket server
    ...
    Methods
    -------
    run()
        run server application        
    """
    def __init__(self):
        """
        Parameters
        ----------
        ADDRESS : object
            service object to communicate with google calender
        """
        HOST = ""   # Empty string means to listen on all IP's on the machine, also works with IPv6.
                # Note "0.0.0.0" also works but only with IPv4.
        PORT = 63000 # Port to listen on (non-privileged ports are > 1023).
        self.ADDRESS = (HOST, PORT)
    

    def run(self):
        """
        start the socket server 
        """        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDRESS)
            s.listen()

            print("Listening on {}...".format(self.ADDRESS))
            while True:
                print("Waiting for Reception Pi...")
                conn, addr = s.accept()
                with conn:
                    print("Connected to {}".format(addr))
                    print()

                    user = socket_utils.recvJson(conn)
                    print('user: ',user)

                    print("real name: ", user['realName'])
                    print("username: ", user['username'])

                    Menu = libraryMenu(user['username'], user['realName'])
                    Menu.runMenu()  

                    socket_utils.sendJson(conn, { "logout": True })


if __name__ == "__main__":
    server().run()
                    