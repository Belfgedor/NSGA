import numpy as np

#population -> List of Lists of 1/0 (Population)
#probabilityOfCrossover -> 0.0 <= Float Number <= 1.0 (Probability of gen interchange)
#output -> Lists of Lists of 1/0 (Crossovered population)
def CrossoverBinary(Population,probabilityOfCrossover):
    CrossoveredPopulation = []
    for individual in Population:
        SelectedIndividual = np.random.choice(range(len(Population)))
        #print SelectedIndividual
        #objective_individual = Population[SelectedIndividual] if Population[SelectedIndividual] != individual else Population[(SelectedIndividual+1) % len(Population)]
        objective_individual = Population[SelectedIndividual]
        individuals_son = []
        for i in xrange(len(individual)):
            individuals_son.append( 
            [objective_individual[i][j] if (probabilityOfCrossover > np.random.rand()) else individual[i][j] for j in xrange(len(individual[i]))]
                )
        #print individual,objective_individual,individuals_son
        CrossoveredPopulation.append(individuals_son)
    return CrossoveredPopulation

def BLX(gen0,gen1,alpha):
    if gen0 == gen1 : return gen0
    gens = sorted([gen0,gen1])
    rang = [gens[0] - alpha*(gens[1]-gens[0]),gens[1] + alpha*(gens[1]-gens[0])]
    return (np.random.rand() * (rang[1]-rang[0])) - rang[0]

#population -> List of List of floats (Population)
#alpha=0.5 -> 0.0 <= Float Number <= 1.0 (extra area for blend; by default 0.5 becouse reomended by experts!!)
#output -> Lists of List of floats (Crossovered population)
def CrossoverBlender(Population, alpha=0.5):
    CrossoveredPopulation = []
    for ind in xrange(len(Population)):
        individual = Population[ind]
        SelectedIndividual = np.random.choice(range(len(Population)))
        objective_individual = Population[SelectedIndividual] if SelectedIndividual != ind else Population[(SelectedIndividual+1) % len(Population)]
        individuals_son = [BLX(objective_individual[i],individual[i],alpha) for i in xrange(len(individual))]
        #print individual,objective_individual,individuals_son
        CrossoveredPopulation.append(individuals_son)
    return CrossoveredPopulation