import numpy as np

#individual -> List of floats
#variance -> Float Number (Varaince for normal function)
#output -> List of loats (mutated individual)
def MutationRealNormal(individual, variance):
    return np.asanyarray([x+np.random.randn()*variance for x in individual])

#individual -> List of 1/0
#variance -> 0.0 <= Float Number <= 1.0 (Varaince for normal function)
#output -> List of 1/0 (mutated individual)
def MutationBinary(Individual, probabilityOfMutation):
    mutated_son = []
    for ind in Individual:
        mutated_son.append([int((not i)) if (probabilityOfMutation > np.random.rand()) else i for i in ind])
    return mutated_son