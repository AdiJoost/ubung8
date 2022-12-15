import pandas as pd
import os
"""
Group is still: Sangeeths and Adrian
"""

def main():
    df = getDataMagic("earthquakes.csv")
    flags = {
        "fromLongitude": -10,
        "toLongitude": 50,
        "fromLatitude": 10,
        "toLatitude": 35,
        "gran": 5
    }
    endList = filterList(df, **flags)
    for entrie in endList:
        print(entrie)

def filterList(df, fromLongitude=0, toLongitude=35, fromLatitude=30, toLatitude=35, gran=1):
    df.loc[df["latd"] == "S", ["lat"]] = -df["lat"]
    df.loc[df["longd"] == "E", ["long"]] = -df["long"]
    return_value = []
    for i in range(fromLatitude, toLatitude, gran):
        filteredFrame = df.loc[df["lat"].between(i, i+gran)]
        for j in range(fromLongitude, toLongitude, gran):
            totF = filteredFrame.loc[df["long"].between(j, j+gran)]
            return_value.append({
                "minLat":i, "minLong":j,
                "entries": totF[["date", "depth", "mag"]].values.tolist()
            })
    return return_value

def getDataMagic(filename="earthquakes.csv"):
    df = pd.read_csv(getDataPath(filename), sep=",", on_bad_lines="skip")
    df['long'] = df['long'].astype(float)
    df['lat'] = df['lat'].astype(float)
    df['depth'] = df['depth'].astype(float)
    df["date"] = pd.to_datetime(df["date"])
    return df

def getDataPath(filename):
    my_path = os.getcwd().split("ubung8", 1)[0]
    return os.path.join(my_path, "ubung8", "data", filename)

def getMe(fromLongitude=0, toLongitude=35, fromLatitude=30, toLatitude=35, gran=1) -> list:
    #returns the filtered List from this exercise
    df = getDataMagic("earthquakes.csv")
    flags = {
        "fromLongitude": fromLongitude,
        "toLongitude": toLongitude,
        "fromLatitude": fromLatitude,
        "toLatitude": toLatitude,
        "gran": gran
    }
    return filterList(df, **flags)

if __name__ == "__main__":
    main()