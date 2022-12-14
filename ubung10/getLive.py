import requests
import os
import json
from datetime import datetime, timedelta
from filelock import FileLock
import pandas as pd

class Earthquicky():

    BASE_URL = "https://seismicportal.eu/fdsnws/event/1/"
    BASE_URL2 = "https://earthquake.usgs.gov/fdsnws/event/1/"
    BL = "https://earthquake.usgs.gov/fdsnws/event/1/"

    

    def __init__(self, rawData=None, startTime=None, endTime=None):
        self.lockPath = self.__getDataPath("earthquakes.csv.lock")
        self.filename = "earthquakes.csv"
        self.filePath = self.__getDataPath(self.filename)
        self.fileLock = FileLock(self.lockPath, 3600)
        self.startTime = startTime
        self.endTime = endTime
        self.rawData = rawData
        self.request = None
        self.__refineData()

    def getLatestDate(self):
        df = self.getDF()
        return df.iloc[-1][0]

    def setStartTime(self, date):
        self.startTime = f"{date.year}-{date.month}-{date.day}"

    def setEndTime(self, date):
        self.endTime = f"{date.year}-{date.month}-{date.day}"

    def GET(self):
        now = datetime.now()
        tail = f"query?format=csv&starttime={self.startTime}&endtime={self.endTime}"
        fullURL = Earthquicky.BL + tail
        self.request = requests.get(fullURL, verify=False)
        self.rawData = self.request.text
        if self.rawData[:9] == "Error 400":
            return "Error 400"
        self.__refineData()
        return "200 - ok"
    
    def getDF(self):
        with self.fileLock:
            df = pd.read_csv(self.__getDataPath(self.filename), sep=",", on_bad_lines="skip")
            df['long'] = df['long'].astype(float)
            df['lat'] = df['lat'].astype(float)
            df['depth'] = df['depth'].astype(float)
            df["date"] = pd.to_datetime(df["date"])
            df.loc[df["latd"] == "S", ["lat"]] = -df["lat"]
            df.loc[df["longd"] == "E", ["long"]] = -df["long"]
            df = df.drop("_id", axis=1)
        return df

    def __getDataPath(self, filename):
        my_path = os.getcwd().split("ubung8", 1)[0]
        return os.path.join(my_path, "ubung8", "data", filename)
    
    def __refineData(self):
        if not self.rawData:
            self.data = None
            return
        rows = self.rawData.split("\n")
        csvData = {}
        for i in range(1, len(rows) - 1):
            args = rows[i].split(",")
            
            eqID = args[11]
            date = args[0]
            try:
                lat = abs(float(args[1]))
                latd = "N" if float(args[1]) >= 0 else "S"
                long = abs(float(args[2]))
                longd = "W" if float(args[2]) >= 0 else "E"
            except ValueError:
                continue
            depth = args[3]
            mag = args[4]
            try:
                if (float(mag) < 0 or float(depth) < 0):
                    continue
            except ValueError:
                continue
            csvData[eqID] = (
                date,
                lat,
                latd,
                long,
                longd,
                depth,
                mag,
                eqID
            )
        self.data = csvData
        self.__removeDoubleID()
    
    def save(self):
        if not self.data:
            return -1
        with self.fileLock:
            with open(self.filePath, "a") as file:
                for key in self.data:
                    file.write("\n")
                    file.write(self.__getCSV(self.data[key]))

    def __getCSV(self, entry):
        returnValue = ""
        for i in range (len(entry) - 1):
            returnValue += str(entry[i])
            returnValue += ","
        returnValue += entry[-1]
        return returnValue

    def __removeDoubleID(self):
        with self.fileLock:
            ids = pd.read_csv(self.filePath, usecols=["_id"])
        copyData = self.data.copy()
        for key in self.data:
            if key in ids.values:
                del copyData[key]
        self.data = copyData



def main():
    myDUDE = Earthquicky()
    startTime = myDUDE.getLatestDate()
    endTime = startTime + timedelta(days=3)
    myDUDE.setStartTime(startTime)
    myDUDE.setEndTime(endTime)
    myDUDE.GET()
    myDUDE.save()
    print(myDUDE.getLatestDate())

if __name__ == "__main__":
    main()

