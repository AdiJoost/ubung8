import requests
import os
import json

class Earthquicky():

    BASE_URL = "https://seismicportal.eu/fdsnws/event/1/"
    BASE_URL2 = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-02"

    

    def __init__(self, data=None, startTime=None, endTime=None):
        self.startTime = startTime
        self.endTime = endTime
        self.data = data
        self.request = None
        self.dataPath = "/datasets/"

    def GET(self):
        tail = f"query?format=geojson&starttime=2014-01-01&endtime=2014-01-02"
        fullURL = Earthquicky.BASE_URL2 + tail
        self.request = requests.get(fullURL, verify=False)
        self.data = self.request.text.replace("\\", "")

    def toJson(self):
        return json.dumps(self.data)

    
    def save(self, filename):
        my_path = os.getcwd().split("ubung8", 1)[0]
        my_path = os.path.join(my_path, "ubung8", "api", "datasets", f"{filename}.json")
        if not self.data:
            return -1
        with open(my_path, "w") as file:
            file.write(self.data)
        return f"{filename}.json"

    @classmethod
    def load(cls, filename):
        my_path = os.getcwd().split("ubung8", 1)[0]
        my_path = os.path.join(my_path, "ubung8", "api", "datasets", f"{filename}.json")
        if not os.path.isfile(my_path):
            return None
        with open(my_path, "r") as file:
            data = file.read()
        return cls(data=data)



def main():


    myDUDE = Earthquicky.load("hello")
    print(myDUDE.data)

if __name__ == "__main__":
    main()

