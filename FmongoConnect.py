from pymongo import MongoClient, server_api
from pymongo.collection import Collection
from bson.objectid import ObjectId


class Event:

    def __init__(self, author: str, msg: str, timeCreated: str, flag: list, severity: float, category: str) -> None:
        self.author = author
        self.msg = msg
        self.timeCreated = timeCreated
        self.flag = flag
        self.severity = severity
        self.category = category
        self.event =    {"id": author,  # data to be stored
                        "msg": msg,
                        "hateIndex": severity,
                        "flagWords": flag,  # flagged words
                        "time": timeCreated,
                        "category": category}


class Backend:
    
    UserTable = 'User Table'
    EventTable = "EventTable"
    CategoryTable = 'CategoryTable'
    
    
    def __init__(self, uriToken: str, certificate: str):
        # initializing connection to the cluster
        self.client = MongoClient(uriToken,
                                  tls = True,
                                  tlsCertificateKeyFile = certificate,
                                  server_api = server_api.ServerApi('1'))
        self.db = self.client['ThehatefulDatabase']
        self.uri = uriToken

    
    # gets a collection from the DB
    def getCollection(self, collection: str) -> Collection:
        # getting collection table
        output = self.db[collection]
        return output

    # returns Id of user, if they don't exist they get put in the system and returns their Id
    def exists(self, username: str) -> ObjectId:
        userTable = self.getCollection(self.UserTable)
        query = {"DiscordId":username}
        cursor = userTable.find(query)
        cursorSize = userTable.count_documents(query)
        
        # Getting User ObjectId
        if cursorSize == 1:
            id = cursor[0]["_id"]
            return id
        
        # Accounting for Users First Offence
        elif cursorSize == 0:
            userTable.insert_one(query)
            cursor = userTable.find(query)
            id = cursor[0]["_id"]
            return id
      
    # creates an entry in EventTable and CategoryTable  
    def log(self, event: Event):
        # getting user Identifier
        id = self.exists(event.author)
        
        # Formatting query
        queryA = {"User id": id,
                "msg": event.msg,
                "hateIndex": event.severity,  
                "flagWords": event.flag,  
                "time": event.timeCreated,
        }
        
        # Inserting Query into EventTable
        eventTable = self.getCollection(self.EventTable)
        eventTable.insert_one(queryA)
        
        # Getting event Id to put into CategoryTable
        cursor = eventTable.find(queryA)
        eventId = cursor[0]['_id']
        
        # inserting the event into the categoryTable
        categoryTable = self.getCollection(self.CategoryTable)
        queryB = {"User id": id,
                  "Event id": eventId,
                  "Category": event.category}
        categoryTable.insert_one(queryB)
        
    # returns the average hatescore of the user
    def userScore(self, username: str) -> int:
        # Connecting to the Collections
        userTable = self.getCollection(self.UserTable)
        queryA = {"DiscordId":username}
        
        # getting user ObjectId
        cursor = userTable.find(queryA)
        id = cursor[0]['_id']
        
        # Getting all instances Instances of User Score
        eventTable = self.getCollection(self.EventTable)
        queryB = {"User id":id}
        cursor = eventTable.find(queryB)
        
        # computing Average hateScore
        numerator = 0
        denominator = 1
        for document in cursor:
            denominator += 1
            temp = 100 * document["hateIndex"]
            numerator += temp
            
        # returning average
        
        return int(numerator/denominator) 
    
    # returns a count of all events with that flag word by that user
    def wordCount(self, word: str, username: str) -> int:
        # Connecting to the Collections
        userTable = self.getCollection(self.UserTable)
        queryA = {"DiscordId":username}
        
        # getting user ObjectId
        cursor = userTable.find(queryA)
        id = cursor[0]['_id']
        
         # Getting all instances Instances of User Score
        eventTable = self.getCollection(self.EventTable)
        queryB = {"User id":id, "flagWords": word}
        return eventTable.count_documents(queryB)
    
    # returns a count of all events of that category by that user
    def categoryCount(self, category: str, username: str) -> int:
        # Connecting to the Collections
        userTable = self.getCollection(self.UserTable)
        queryA = {"DiscordId":username}
        
        # getting user ObjectId
        cursor = userTable.find(queryA)
        id = cursor[0]['_id']
        
        # Getting all instances Instances of User Score
        eventTable = self.getCollection(self.CategoryTable)
        ape = eventTable.distinct("Category")
        print(type(ape[2]))
        queryB = {"User id":id, "Category": category}
        return eventTable.count_documents(queryB)
     
    #  returns a count of all events by that user
    def allEventCount(self, username: str) -> int:
        # Connecting to the Collections
        userTable = self.getCollection(self.UserTable)
        queryA = {"DiscordId":username}
        
        # getting user ObjectId
        cursor = userTable.find(queryA)
        id = cursor[0]['_id']
        
         # Getting all instances Instances of User Score
        eventTable = self.getCollection(self.EventTable)
        queryB = {"User id":id}
        return eventTable.count_documents(queryB)
