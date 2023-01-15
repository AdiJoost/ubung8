from pseudocode import getDataMagic
from datetime import datetime, timedelta
import pandas as pd

def filterFrame(df, mag=None, depth=None, date=None):
    returnValue = df
    #date = (date, date + timedelta(1))
    if mag:
        returnValue = returnValue.loc[returnValue["mag"] == mag]
    if depth:
        returnValue = returnValue.loc[returnValue["depth"] == depth]
    if date:
        returnValue = returnValue.loc[returnValue["date"].between(date[0], date[1])]
    return returnValue

def main():
    df = getDataMagic()
    df["date"] = pd.to_datetime(df["date"])
    flags = {
        "mag": (1.2),
        "depth": (44.6),
        "date":("2014-1-1", "2014-1-3")
    }
    print("df before filtering")
    print(df.head())
    df = filterFrame(df, **flags)
    print("df after filtering")
    print(df.head())


if __name__ == "__main__":
    main()