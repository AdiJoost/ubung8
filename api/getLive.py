import requests
import os

class Earthquicky():

    BASE_URL = "https://seismicportal.eu/fdsnws/event/1/"
    BASE_URL2 = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-02"

    

    def __init__(self, startTime, endTime=None):
        self.startTime = startTime
        self.endTime = endTime
        self.data = None

    def GET(self):
        tail = f"query?limit=10&start={self.startTime}&format=json"
        tail = "version"
        fullURL = Earthquicky.BASE_URL + tail
        cafile = os.path.join(Earthquicky.getSubPath(), "cacert.pem")
        print(cafile)
        self.data = requests.get(Earthquicky.BASE_URL2, verify=False)

    @classmethod
    def getSubPath(cls):
        my_path = os.getcwd().split("ubung8", 1)[0]
        return os.path.join(my_path, "ubung8", "api")


def main():
    earthy = Earthquicky("2022-08-01")
    earthy.GET()
    print(earthy.data)

if __name__ == "__main__":
    main()

