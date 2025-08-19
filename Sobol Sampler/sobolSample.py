'''
@author Mason Fox
date: 08 OCT 2023

Sobol Method Script
Purpose: Generate sobol samples for use in sensitivity driver script. Allows screening of larger number of parameters.
Inputs: Symbolic functions/correlations from uncertainFunctions.py, values of uncertain parameters, number of 
Outputs: CSV with information for each run, interface for external simulation driver script
'''

import math
from dataclasses import dataclass
from enum import Enum
from SALib.sample import sobol
from os import path
import numpy as np
import _pickle as pickle
from Sobol_Method import sobolFunctions, genPowerPulse
from pprint import pprint

def main():
    #need fuel params for energydep/pulsewidth to W/m^3
    l = 0.1 #m
    r = 4.096E-3 #m
    volFuel = math.pi * r**2 * l #m^3
    densFuel = 10421.5

    sobolPklFn = "sobolProblem_revise.pkl"

    #use to generate a new sobol problem and save to pkl
    #sensitivityProblem = gen_initial_samples(sobolPklFn, 1024, volFuel, densFuel)
    
    #use to append already existing sobol problem from a pkl file
    sensitivityProblem = append_additional_samples(sobolPklFn, 1024, volFuel, densFuel, 1024)

    pklPath = path.dirname(__file__) + '/' + sobolPklFn #relative path instead of calling path
    #save problem with run data to disk using pickle
    with open (pklPath, 'wb') as outpb:
        pickle.dump(sensitivityProblem, outpb, -1)

@dataclass
class simulationRunInputs():
    """Store info with functions and values for each parameter in a single simulation"""
    paramVals : list
    numParams : int = 0
    
    def addParam(self, paramDat:float):
        self.numParams = self.numParams+1
        self.paramVals.append(paramDat)

    def getParams(self) -> list:
        return self.paramVals

@dataclass
class problem():
    problemDef : dict
    runsList : list
    numRuns : int = 0
    numParams : int = 0

    def addRun(self, runDat:simulationRunInputs):
        self.numRuns = self.numRuns + 1
        self.runsList.append(runDat)

    def getRun(self, index:int) -> simulationRunInputs:
        return self.runsList[index]

    def getNumRuns(self) -> int:
        return self.numRuns

    def getNames(self) -> list:
        return self.problemDef['names']

def append_additional_samples(sobolPklFn, n_sobol, 
                              volFuel, densFuel, skipNum):
    
    pklPath = path.dirname(__file__) + '/' + sobolPklFn #relative path instead of calling path
   
    #load existing problem
    with open (pklPath, 'rb') as inpb:
        sensitivityProblem = pickle.load(inpb)

    sobolArr = sampler(sensitivityProblem, n_sobol, False, skip_vals=skipNum) #skip_vals for second batch
    arrayToInputs(sensitivityProblem, sobolArr, volFuel, densFuel)
    print("Total Num Runs: ", sensitivityProblem.getNumRuns())

    return sensitivityProblem

def gen_initial_samples(sobolPklFn, n_sobol, volFuel, densFuel):
    #initialize problem (no runs yet)
    problemDefDict = sobolFunctions.defineParams()
    numParameters = len(problemDefDict['names'])
    
    pklPath = path.dirname(__file__) + '/' + sobolPklFn #relative path instead of calling path
    
    #generate problem and add run inputs
    sensitivityProblem = problem(problemDefDict, runsList=[], numParams=numParameters)
    
    sobolArr = sampler(sensitivityProblem, n_sobol, False)
    arrayToInputs(sensitivityProblem, sobolArr, volFuel, densFuel)
  
    return sensitivityProblem

def sampler(problemDetails:problem, n_run_mult:int, calc_second_ord:bool, skip_vals=0):
    """Builds sensitivity problem and performs sobol sampling.
    ============================================================================
    n_run_mult: multiplier for number of runs -- #runs = n_run_mult * (#params + 2) as defined by sobol
    """

    #build problem
    if n_run_mult % 2 != 0:
        raise Exception("Sobol parameter (n_run_mult) should be a power of 2.")

    #sample
    sampleArray = sobol.sample(problemDetails.problemDef, n_run_mult, 
                               calc_second_order=calc_second_ord, skip_values=skip_vals)    

    print("Num Runs Generated: ", len(sampleArray))
    return sampleArray

def arrayToInputs(prob:problem, arr:np.ndarray, fuelVol:float, fuelDens:float):
    """Convert ndarray from sampler into uncertain_parameter. Assign uncertain_parameter into simulationRunInputs object"""
    
    varNameList = prob.problemDef['names']
    pw = -1
    edep = 150 #-1

    for runSet in arr:
        newRun = simulationRunInputs([], 0)
        for n, item in enumerate(runSet):
            newRun.addParam(item)

            if 'pulse_width' in varNameList[n]:
                pw = item
            elif 'energyDep' in varNameList[n]:
                edep = item
        
        if (pw == -1):
            raise Exception('Pulse width value invalid.')
        elif (edep == -1):
            raise Exception('Energy deposition value invalid.')
        else:
            power = genPowerPulse.genPowerCurve(edep, pw, fuelVol, fuelDens, numPts=250)     #default m=9.1g, numpts = 1000

        newRun.addParam(power)
        prob.addRun(newRun)

if __name__ == '__main__':
    main()
