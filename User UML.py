import datetime

class user:
    def __init__(self, name: str):
        self.name = name
        # add later on a global id counter that increases each time
        self.id = 0
        self.status = 'active'
        
    def get_name(self):
        return self.name
    
class calenderEvent:
    def __init__(self, datetime: datetime, name: str, description: str, 
                 location: str, duration: int, participants: list, 
                 creator: user, id: int, priority: int):
        self.datetime = datetime
        self.name = name
        self.description = description
        self.location = location
        self.duration = duration
        self.participants = participants
        self.creator = creator
        self.id = id
        self.priority = priority

    def editEvent(self, datetime: datetime, name: str, description: str, 
                  location: str, duration: int, participants: list, 
                  creator: user, id: int, priority: int):
        self.datetime = datetime
        self.name = name
        self.description = description
        self.location = location
        self.duration = duration
        self.participants = participants
        self.creator = creator
        self.id = id
        self.priority = priority

    # muss eventuell noch angepasst werden
    def deleteEvent(self):
        self.datetime = None
        self.name = None
        self.description = None
        self.location = None
        self.duration = 0
        self.participants = []
        self.creator = None
        self.id = 0
        self.priority = 0

class location:
    # muss nochmal schauen ob das so passt, bzw. ob du andere parameter brauchst
    def __init__(self, name: str, description: str, address: str, 
                 openingHours: str, id: int):
        self.name = name
        self.description = description
        self.address = address
        self.openingHours = openingHours
        self.id = id

    def editLocation(self, name: str, description: str, address: str, 
                     openingHours: str, id: int):
        self.name = name
        self.description = description
        self.address = address
        self.openingHours = openingHours
        self.id = id

    def deleteLocation(self):
        self.name = None
        self.description = None
        self.address = None
        self.openingHours = None
        self.id = 0

class calenderGUI:
    def __init__(self, view: str, startDate: datetime):
        self.view = view
        self.startDate = startDate

        
    
    
    
    
