from pseudocode import getDataMagic
from datetime import datetime
import pandas as pd

def filterFrame(df, mag=None, depth=None, date=None):
    returnValue = df
    if mag:
        returnValue = returnValue.loc[returnValue["mag"].between(mag[0], mag[1])]
    if depth:
        returnValue = returnValue.loc[returnValue["depth"].between(depth[0], depth[1])]
    if date:
        returnValue = returnValue.loc[returnValue["date"].between(date[0], date[1])]
    return returnValue

def main():
    df = getDataMagic()
    flags = {
        "date":(datetime(2016, 1, 1), datetime(2016,12,31))
    }
    df = filterFrame(df, **flags)
    print(df.describe())


if __name__ == "__main__":
    main()