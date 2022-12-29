import requests
import os
import json
from datetime import datetime
from filelock import FileLock
import pandas as pd

class Earthquicky():

    BASE_URL = "https://seismicportal.eu/fdsnws/event/1/"
    BASE_URL2 = "https://earthquake.usgs.gov/fdsnws/event/1/"
    BL = "https://earthquake.usgs.gov/fdsnws/event/1/"

    

    def __init__(self, data=None, startTime=None, endTime=None):
        self.lockPath = self.__getDataPath("earthquakes.csv.lock")
        self.filename = "earthquakes.csv"
        self.fileLock = FileLock(self.lockPath, 3600)
        self.startTime = startTime
        self.endTime = endTime
        self.data = data
        self.request = None

    def GET(self):
        now = datetime.now()
        tail = f"query?format=csv&starttime=2000-01-01&endtime=2014-01-02"
        fullURL = Earthquicky.BL + tail
        self.request = requests.get(fullURL, verify=False)
        self.data = self.request.text
    
    def getDF(self):
        with self.fileLock:
            df = pd.read_csv(self.__getDataPath(self.filename), sep=",", on_bad_lines="skip")
            df['long'] = df['long'].astype(float)
            df['lat'] = df['lat'].astype(float)
            df['depth'] = df['depth'].astype(float)
            df["date"] = pd.to_datetime(df["date"])
            df.loc[df["latd"] == "S", ["lat"]] = -df["lat"]
            df.loc[df["longd"] == "E", ["long"]] = -df["long"]
        return df

    def __getDataPath(self, filename):
        my_path = os.getcwd().split("ubung8", 1)[0]
        return os.path.join(my_path, "ubung8", "data", filename)

    def loadCSV():
        pass
        



def main():

    myDUDE = Earthquicky()
    df = myDUDE.getDF()
    print(df.head())

if __name__ == "__main__":
    main()

