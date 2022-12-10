from aufgabe41 import getData
from mag_depth_matrix import MagDepthMatrix

def main():
    df = getData("earthquakes.csv")
    magRange = (df["mag"].min(), df["mag"].max())
    depthRange = (df["depth"].min(), df["depth"].max())
    matrix = MagDepthMatrix(df=df, magRange=magRange, depthRange=depthRange)
    for row in matrix.matrix:
        print(row)

    



if __name__ == "__main__":
    main()