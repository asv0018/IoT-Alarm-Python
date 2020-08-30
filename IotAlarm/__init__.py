import time
from datetime import datetime

import pyrebase
import json
import requests
from firebasedata import LiveData


class IotConnectivity:
    def __init__(self, configFile):
        self.__serial_num = "test"
        self.__configFile = configFile
        self.__firebase = None
        self.connection_exist = False
        self.condition_init = False
        self.event = ""
        self.data = ""
        self.path = ""
        self.dictionary = ""

    def initialise(self):
        self.connection_exist = self.__checkInternet()
        if self.connection_exist:
            file = open(self.__configFile, )
            config = json.load(file)
            file.close()
            self.__firebase = pyrebase.initialize_app(config)

        else:
            print("exiting, due to no internet connectivity")

    def __checkInternet(self):
        response = None
        try:
            response = requests.get("https://google.com/", timeout=5)
            print("Connection exists")
            return True
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("connection error")
            return False

    def getLocationOnIP(self):
        response = requests.get("http://ipinfo.io/json")
        data = json.load(response.text)
        return data

    def isTimeInSync(self):
        pass

    def setTimeBeforeUse(self):
        pass

    def stream_handler(self, response):
        self.event = response["event"]
        self.path = response["path"]
        temp = response["data"]
        if self.condition_init is False:
            self.data = temp
            self.condition_init = True
        else:# find a path where the data needs to be inserted to and set it#patharray = self.path.slice("/")
            pass

        #print(self.event + " is the event")
        ##print(self.path + " is the path")
        #print(str(self.data) + " is the data")

        # self.data = json.load(data)
        # print(str(data))
    def handler(self, data):
        print(data)

    def run(self):
        firebase = self.__firebase
        registered_uid = self.__firebase.database().child("iot_alarm").child(self.__serial_num).child(self.__serial_num)
        registered_uid = registered_uid.get().val()
        print("registered uid is : " + registered_uid)
        db = firebase.database()
        live = LiveData(self.__firebase, '/alarms_users')
        live.signal('/registered_uid').connect(self.handler)
        self.data = live.get_data()
        while True:

             if self.data != "":
                 while True:
                     now = datetime.now()
                     current_time = now.strftime("%H:%M")
                     #print("current time : " + current_time)

