
class MagDepthMatrix ():
    #This Class calculates a desety-Matrix for the earthquake-dataset.
    #You can sepcify a range for depth and magnitude of the resulting Matrix
    #The matrixDim is the resolution of the matrix. The class calculates the
    #given intervalls of the rows and columns automatically.

    def __init__ (self, df=None, magRange=(0, 10), depthRange= (0,100), matrixDim=20):
        self.df = df
        self.magRange = magRange
        self.depthRange = depthRange
        self.matrixDim = matrixDim
        self.matrix = [[0] * matrixDim for _ in range(matrixDim)]
        self.matrixFilters = self.getFilter()
        self.fillMatrix()
    
    def getMatrixMagic(self):
        returnValue =[[]]
        for i in range(self.matrixDim):
            row = []
            for j in range(self.matrixDim):
                row.append((self.matrix[i][i], self.matrixFilters))
            returnValue.append(row)
        return returnValue

    def fillMatrix(self):
        for i in range(self.matrixDim - 1):
            filteredDf = self.df.loc[self.df["mag"].between(self.matrixFilters[i][0][0], self.matrixFilters[i + 1][0][0])]
            for j in range(self.matrixDim - 1):
                dff = filteredDf.loc[filteredDf["depth"].between(self.matrixFilters[0][j][1], self.matrixFilters[0][j + 1][1])]
                self.matrix[i][j] = len(dff)
            dff = filteredDf.loc[filteredDf["depth"] > self.matrixFilters[0][self.matrixDim - 1][1]]
            self.matrix[i][self.matrixDim - 1] = len(dff)

        filteredDf = self.df.loc[self.df["mag"] >= self.matrixFilters[self.matrixDim - 1][0][0]]
        for j in range(self.matrixDim - 1):
            dff = filteredDf.loc[filteredDf["depth"].between(self.matrixFilters[0][j][1], self.matrixFilters[0][j + 1][1])]
            self.matrix[self.matrixDim - 1][j] = len(dff)

        dff = filteredDf.loc[filteredDf["depth"] > self.matrixFilters[0][self.matrixDim - 1][1]]
        self.matrix[self.matrixDim - 1][self.matrixDim - 1] = len(dff)

    def getFilter(self):
        magStepSize = (self.magRange[1] - self.magRange[0]) / self.matrixDim
        self.magStep = magStepSize
        depthStepSize = (self.depthRange[1] - self.depthRange[0]) / self.matrixDim
        self.depthStep = depthStepSize
        returnValue = []
        for i in range(self.matrixDim):
            magVal = (round((self.magRange[0] + i*magStepSize), 2))
            currentRow = []
            for j in range(self.matrixDim):
                currentRow.append((magVal, round((self.depthRange[0] + j*depthStepSize), 2)))
            returnValue.append(currentRow)
        return returnValue
