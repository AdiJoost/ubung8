import requests
import os
import json

class Earthquicky():

    BASE_URL = "https://seismicportal.eu/fdsnws/event/1/"
    BASE_URL2 = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-02"

    

    def __init__(self, startTime, endTime=None):
        self.startTime = startTime
        self.endTime = endTime
        self.data = None
        self.request = None
        self.dataPath = "/datasets/"

    def GET(self):
        tail = f"query?format=geojson&starttime=2014-01-01&endtime=2014-01-02"
        fullURL = Earthquicky.BASE_URL2 + tail
        self.request = requests.get(fullURL, verify=False)
        self.data = self.request.text

    def toJson(self):
        return json.dumps(self.data)
    
    def save(self, filename):
        my_path = os.getcwd().split("ubung8", 1)[0]
        my_path = os.path.join(my_path, "ubung8", "api", "datasets", f"{filename}.json")
        if not self.data:
            return -1
        with open(my_path, "w") as file:
            file.write(json.dumps(self.data))
        return f"{filename}.json"



def main():
    earthy = Earthquicky("2022-08-01")
    earthy.GET()
    #print(earthy.toJson())
    print(earthy.save("hello"))

if __name__ == "__main__":
    main()

