import socket, json, sqlite3
import socket_utils

class socketClient:
    """
    A class used to handle socket connection for client side
    ...
    Methods
    -------
    generateJsonData(username,realName)
        generate json data 
    mainRun()
        load the json file 
    """    
    def __init__(self,username,realName):
        """
        Parameters
        ----------
        username : str
           user name
        realName : str
            user real name                                                                                      
        """        
        with open("socketConfig.json", "r") as file:
            data = json.load(file)
            host = data["masterpi_ip"] # The server's hostname or IP address.
            port = data["masterpi_port"]# The port used by the server.
            self.ADDRESS = (host, int(port))
        self.jsonData=self.generateJsonData(username,realName)
    
    #generate json data
    def generateJsonData(self,username,realName):
        """
        Parameters
        ----------
        username : str
           user name
        realName : str
            user real name                                                                                      
        """        
        return {"username": username, "realName": realName}

    #maun run to connect with server
    def mainRun(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(self.ADDRESS))
            s.connect(self.ADDRESS)
            print("Connected.")

            print("Logging in as {}".format(self.jsonData))
            socket_utils.sendJson(s, self.jsonData)

            print("Waiting for Master Pi...")
            while(True):
                object = socket_utils.recvJson(s)
                if("logout" in object):
                    print("Master Pi logged out.")
                    print()
                    break    