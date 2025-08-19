import pickle as pkl
from dataclasses import dataclass

@dataclass
class simulationRunInputs():
    paramVals: list
    numParams: int = 0

    def addParam(self, paramDat:float):
        self.numParams = self.numParams + 1
        self.paramVals.append(paramDat)

    def getParams(self):
        return self.paramVals

@dataclass
class problem():
    problemDef : dict
    runsList : list
    numRuns : int = 0
    numParams : int = 0

    def addRun(self, runDat):
        self.numRuns = self.numRuns+1
        self.runsList.append(runDat)

    def getRun(self, index):
        return self.runsList[index]

    def getNumRuns(self):
        return self.numRuns

    def getNames(self):
        return self.problemDef['names']

def main():
    with open('sobolProblem_revise.pkl', 'rb') as fn:
        problem = pkl.load(fn)

    ##print(problem)
    numRuns = problem.getNumRuns()
    print(problem.getNames())
    #print(problem.getRun(416))

    for i in range(0,numRuns):
        thisRunParams = problem.getRun(i).getParams()
        #print power
        #print(thisRunParams[-1])
        #print pw, edep
        print(i, [float(param) for param in thisRunParams[:-1]])

main()
