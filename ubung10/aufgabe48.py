from aufgabe47 import filterFrame
from myUtils import getData
from datetime import datetime
import pandas as pd

def calcMean(df, dates):
    df = filterFrame(df, date=dates)
    depthMean = df["depth"].mean()
    magMean = df["mag"].mean()
    return (depthMean, magMean)

def slidingTW(df, startTime, endTime, intervall=10, steps=3):
    #intervall in days, steps in days
    returnValue = []

def main():
    df = getData()
    print(calcMean(df, (datetime(2017,1,1), datetime(2017,12,31))))



if __name__ == "__main__":
    main()