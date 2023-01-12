from aufgabe47 import filterFrame
from pseudocode import getDataMagic
from datetime import datetime, timedelta
import pandas as pd

def calcMean(df, dates):
    df = filterFrame(df, date=dates)
    depthMean = df["depth"].mean()
    magMean = df["mag"].mean()
    return (depthMean, magMean)

def slidingTW(df, startTime, endTime, intervall=10, steps=3):
    #intervall in days, steps in days
    returnValue = []
    
    return returnValue

def getMeanMagic(df, startDate, endDate, intervall):
    #Input: DF, 
    timeDate = getDates(startDate, endDate, intervall)
    getMeanMagicDF = pd.DataFrame(columns=[
        "startDate",
        "endDate",
        "meanMag",
        "meanDepth"])
    for i in range(len(timeDate) -1):
        depthMean, magMean = calcMean(df, (timeDate[i], timeDate[i+1]))
        getMeanMagicDF.loc[i] = [timeDate[i], timeDate[i+1], magMean, depthMean]
    return getMeanMagicDF

def getDates(startDate, endDate, intervall):
    returnValue = []
    totalTime = endDate - startDate
    print(totalTime)
    for i in range(0, totalTime.days, intervall):
        returnValue.append(startDate + timedelta(i))
    return returnValue

def main():
    df = getDataMagic()
    print(getMeanMagic(df, df.iloc[0,0], df.iloc[len(df)-1,0], 3))




if __name__ == "__main__":
    main()