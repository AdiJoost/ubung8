import pandas as pd
from aufgabe41 import getMe

def main():
    flags = {
        "fromLongitude": 10,
        "toLongitude": 50,
        "fromLatitude": 0,
        "toLatitude": 60,
        "gran": 10
    }

    #get List created in exercise 41
    filteredList = getMe(**flags)
    for entrie in filteredList:
        print(calcStats(entrie))
    
def calcStats(entire) -> dict:
    #calculates mean, median, min and max value in
    #a entrie and returns a dict with that values
    returnValue = {
        "depth": {
            "mean": None,
            "median": None,
            "max": None,
            "min":None
        },
        "mag":{
            "mean": None,
            "median": None,
            "max": None,
            "min": None
        }
    }
    df = pd.DataFrame(entire.get("entries"))
    if df.empty:
        return returnValue
    returnValue["depth"]["mean"] = df[df.columns[2]].mean()
    returnValue["depth"]["median"] = df[df.columns[2]].median()
    returnValue["depth"]["max"] = df[df.columns[2]].max()
    returnValue["depth"]["min"] = df[df.columns[2]].min()

    returnValue["mag"]["mean"] = df[df.columns[1]].mean()
    returnValue["mag"]["median"] = df[df.columns[1]].median()
    returnValue["mag"]["max"] = df[df.columns[1]].max()
    returnValue["mag"]["min"] = df[df.columns[1]].min()
    return returnValue
        
    

if __name__ == "__main__":
    main()