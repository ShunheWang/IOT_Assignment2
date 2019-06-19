# Reference: https://developers.google.com/calendar/quickstart/python
# Reference: reference the source code from tutorial provide from RMIT 
# Documentation: https://developers.google.com/calendar/overview


from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pytz import timezone

class calender(object):
    """
    A class used to handle calender process
    ...
    Methods
    -------
    getBorrowedDate()
        get the today borrow date 
    getReturnDate()
        get the return date 
    getReturnDateTime() 
        get the return date and time 
    insertCalender(user, title)
        insert the calender event   
    removeEvent(htmlLink)
        remove calender event        
    """
    def __init__(self):
        """
        Parameters
        ----------
        __service : object
            service object to communicate with google calender
        """
        SCOPES = "https://www.googleapis.com/auth/calendar"
        store = file.Storage("token.json")
        creds = store.get()
        if(not creds or creds.invalid):
            flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
            creds = tools.run_flow(flow, store)
        self.__service = build("calendar", "v3", http=creds.authorize(Http()))

    def getBorrowedDate(self):
        """
        get the today borrow date  
        """ 
        mel_zone = timezone('Australia/Melbourne')
        date = datetime.now(mel_zone)
        today = (date + timedelta(days = 0)).strftime('%Y-%m-%d')
        return today 

    def getReturnDate(self):
        """
        get the today return date  
        """   
        mel_zone = timezone('Australia/Melbourne')
        date = datetime.now(mel_zone)
        returnDate = (date + timedelta(days = 7)).strftime('%Y-%m-%d')
        return returnDate 

    def getReturnDateTime(self): 
        """
        get the return date and time  
        """   
        mel_zone = timezone('Australia/Melbourne')
        date = datetime.now(mel_zone)
        returnDate = (date + timedelta(days = 7)).strftime('%Y-%m-%dT%H:%M:%S')
        return returnDate        

    def insertCalender(self, user, title):
        """
        insert the calender event 

        Parameters
        ----------
        user : string
            User's name
        title : string
            book title    
        """
        tomorrow = self.getReturnDate()
        time_start = self.getReturnDateTime()
        time_end = "{}T17:00:00".format(tomorrow)

        description = "Return book title: " + title + " by borrower: " + user
        event = {
            "summary": "Return book Event",
            "description": description,
            "start": {
                "dateTime": time_start,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "dateTime": time_end,
                "timeZone": "Australia/Melbourne",
            }
        }

        event = self.__service.events().insert(calendarId = "primary", body = event).execute()
        print("Event created: {}".format(event.get("htmlLink")))

        return event.get("htmlLink")

    def removeEvent(self, htmlLink):
        """
        remove the calender event 

        Parameters
        ----------
        htmlLink : string
            html link use by the google calender    
        """  
        events_result1 = self.__service.events().list(calendarId = "primary").execute()   

        for event in events_result1['items']:
            link = event["htmlLink"]

            if (link == htmlLink):
                id = event["id"]
                self.__service.events().delete(calendarId='primary', eventId=id).execute()
                print("delete calender event")
                break
       