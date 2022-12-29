import requests
import os
import json
from datetime import datetime
import Filelock

class Earthquicky():

    BASE_URL = "https://seismicportal.eu/fdsnws/event/1/"
    BASE_URL2 = "https://earthquake.usgs.gov/fdsnws/event/1/"
    BL = "https://earthquake.usgs.gov/fdsnws/event/1/"

    

    def __init__(self, data=None, startTime=None, endTime=None):
        self.startTime = getStartTime()
        self.endTime = endTime
        self.data = data
        self.request = None
        self.dataPath = "/datasets/"

    def GET(self):
        now = datetime.now()
        tail = f"query?format=csv&starttime=2000-01-01&endtime=2014-01-02"
        fullURL = Earthquicky.BL + tail
        self.request = requests.get(fullURL, verify=False)
        self.data = self.request.text
    
    def getStartTime():




def main():


    myDUDE = Earthquicky()
    myDUDE.GET()
    print(myDUDE.data)

if __name__ == "__main__":
    main()

