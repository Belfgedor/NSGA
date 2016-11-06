import numpy as np
#Maximize Objective Functions
#IndividualsRanks -> List of real values (objective funtions outputs)
#NumberOfSelectedIndividuals -> Integer number (number of selected individuals)
#Output : List of integers (positions of the selected individuals)
def StochasticRemainderSelection(IndividualsRanks, NumberOfSelectedIndividuals):
    # 1. ToPercentage + NumberOfSelectedIndividuals
    #We consider that situation when we can want obtain less indiduals tha in the input.
    NPi = NumberOfSelectedIndividuals * (np.asanyarray(IndividualsRanks)*1.0/np.sum(IndividualsRanks)) 
    for i in xrange(len(IndividualsRanks)):
        print  IndividualsRanks[i], NPi[i]
    # 2. Select integer part
    IntegerParts = [int(npi) for npi in NPi]
    Output = []
    for i in xrange(len(IntegerParts)): 
        for j in xrange(IntegerParts[i]):
            Output.append(i)
            #If there are more inger parts or are the same
            
    if NumberOfSelectedIndividuals <= len(Output):
        return Output
    
    IndexesOfRest=[]
    RestParts=[]    
    for i in xrange(len(NPi)): 
        if (NPi[i] - int(NPi[i])) != 0.0:
            IndexesOfRest.append(i)
            #if len(RestParts) == 0:
            #    RestParts.append(0)
            RestParts.append(NPi[i] - int(NPi[i]))
    RestParts = np.asanyarray(RestParts)*1.0/np.sum(RestParts)
    RestPartsRulete = [0.0]
    
    for i in xrange(len(RestParts) ):
        RestPartsRulete.append(RestParts[i] + RestPartsRulete[-1])
    RestPartsRulete = np.asanyarray(RestPartsRulete)
    print RestPartsRulete
    for j in xrange(NumberOfSelectedIndividuals - len(Output)):
        RandomSelection = np.random.rand()
        Selection = np.where(RestPartsRulete <= RandomSelection)[0][-1]
        Output.append(IndexesOfRest[Selection])
    
    return Output