from mag_depth_matrix import MagDepthMatrix
from aufgabe41 import getData
import math
import plotly.express as px


def main():
    df = getData("earthquakes.csv")
    magRange = (df["mag"].min(), df["mag"].max())
    depthRange = (df["depth"].min(), df["depth"].max())
    matrix = MagDepthMatrix(df=df, magRange=magRange, depthRange=depthRange)
    nomMatrix = logMatrix(matrix.matrix)
    fig = px.imshow(
        nomMatrix,
        labels={
            "y": "Depth",
            "x": "Magnitude",
            "color": "logarithmic occurences"
        },
        text_auto=False)
    fig.show()
    printMaxOccurences(matrix)

def logMatrix(matrix):
    returnValue = [[0] * len(matrix) for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if (matrix[i][j] > 0):
                returnValue[i][j] = math.log(matrix[i][j])
    return returnValue

def printMaxOccurences(matrix):
    maxValue = -1
    x = -1
    y = -1
    for i in range(matrix.matrixDim):
        for j in range(matrix.matrixDim):
            if (matrix.matrix[i][j] > maxValue):
                maxValue = matrix.matrix[i][j]
                x = i
                y = j
    print(f"Am Häufigsten tritt das Magnitud-Tiefenpaar von {matrix.matrixFilters[x][y]}"\
        f"nach {(matrix.matrixFilters[x][y][0] + matrix.magStep, matrix.matrixFilters[x][y][1] + matrix.depthStep)} auf")

if __name__ == "__main__":
    main()