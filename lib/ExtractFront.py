import numpy as np

#PopulationFitness -> List of Lists of Float (List of individuals where each of individuals is a list of fitness funtions for the individual)
#output -> A list of integers (List of inxes of the front of the population)
def FrontExtraction(PopulationFitness):
    Front = []
    for ind in xrange(len(PopulationFitness)):
        WeAreOK = True
        for obj in xrange(len(PopulationFitness)):
            if obj==ind : continue
            if sum(PopulationFitness[ind] >= PopulationFitness[obj]) == len(PopulationFitness[obj]):
                break
            if sum(PopulationFitness[ind] > PopulationFitness[obj]) == 0:
                WeAreOK = False
                break
        if WeAreOK:
            Front.append(ind)
    return Front
