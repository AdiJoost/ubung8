from aufgabe47 import filterFrame
from pseudocode import getDataMagic
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

def calcMean(df, dates):
    #gets the mean value from startDate to endDate in dates
    df = filterFrame(df, date=dates)
    depthMean = df["depth"].mean()
    magMean = df["mag"].mean()
    return (depthMean, magMean)

def slidingTW(df, startTime, endTime, intervall=10, steps=3):
    #intervall in days, steps in days
    returnValue = []
    
    return returnValue

def getMeanMagic(df, startDate= pd.to_datetime('2014-01-01T23:51:36.020Z'), endDate=pd.to_datetime('2015-12-25T00:07:27.740Z'), intervall=10):
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
    #Get a list of all Dates from startDate to endDate with an intervall of "intervall"
    returnValue = []
    totalTime = endDate - startDate
    print(totalTime)
    for i in range(0, totalTime.days, intervall):
        returnValue.append(startDate + timedelta(i))
    return returnValue

def plotMeanMagic(df):
    plt.subplot(1,2,1)
    plt.xlabel('Cells')
    plt.ylabel('Timesteps')
    plt.title("Left Lane")
    plt.plot(df["startDate"], df["meanMag"])
    plt.xticks(rotation=90)
    plt.subplot(1,2,2)
    plt.title("Right Lane")
    plt.xlabel('Cells')
    plt.plot(df["startDate"], df["meanDepth"])
    plt.xticks(rotation=90)
    plt.show()

def main():
    df = getDataMagic()
    plotMeanMagic(getMeanMagic(df, df.iloc[0,0], df.iloc[len(df)-1,0], 3))




if __name__ == "__main__":
    main()