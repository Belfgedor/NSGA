import numpy as np

#PopulationFitness -> List of Lists of Float (List of individuals where each of individuals is a list of fitness funtions for the individual)
#SharingFitness -> A float value
#output -> A list of integers (List of inxes of the front of the population)
def FrontExtraction(PopulationFitness):
    Front = []
    for ind in xrange(len(PopulationFitness)):
        WeAreOK = True
        for obj in xrange(len(PopulationFitness)):
            #print "ES Frente?", ind,obj
            if obj==ind : continue
            if sum(PopulationFitness[ind] >= PopulationFitness[obj]) == len(PopulationFitness[obj]):
                #print sum(PopulationFitness[ind] >= PopulationFitness[obj]),(PopulationFitness[ind] >= PopulationFitness[obj]),len(PopulationFitness[obj])
                if not (sum(PopulationFitness[ind] == PopulationFitness[obj]) == len(PopulationFitness[obj])):
                    WeAreOK = False
                    break
            #if sum(PopulationFitness[ind] > PopulationFitness[obj]) == 0:
            #    print (PopulationFitness[ind] > PopulationFitness[obj])
            #    WeAreOK = False
            #    break
        if WeAreOK:
            Front.append(ind)
    return Front