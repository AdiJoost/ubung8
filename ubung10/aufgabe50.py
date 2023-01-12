from aufgabe43 import getMatrix
from aufgabe44 import logMatrix
import plotly.express as px


def main():
    filterSet43()
    filterSet44()

def filterSet43():
    matrix = getMatrix()
    matr = matrix.matrix
    for row in matr:
        row.sort(reverse=True)
    matr.sort(reverse=True)
    for row in matr:
        print(row)
    plotMatirx(matr)

def filterSet44():
    matrix = getMatrix()
    matr = logMatrix(matrix.matrix)
    for row in matr:
        row.sort(reverse=True)
    matr.sort(reverse=True)
    for row in matr:
        print(row)
    plotMatirx(matr)

def plotMatirx(nomMatrix):
    fig = px.imshow(
        nomMatrix,
        labels={
            "y": "Depth",
            "x": "Magnitude",
            "color": "logarithmic occurences"
        },
        text_auto=False)
    fig.show()


if __name__ == "__main__":
    main()
