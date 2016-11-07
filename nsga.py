import numpy as np
import matplotlib.pyplot as plt
from lib.Crossover import CrossoverBinary,CrossoverBlender
from lib.ExtractFront import FrontExtraction
from lib.Mutation import MutationBinary,MutationRealNormal
from lib.SRS import StochasticRemainderSelection
from lib.Sharing import sharing
from copy import deepcopy as dcp

#import lib.tests_nsga as TESTS

def apply_limits(individual,parametrss_limits):
    correct_individual = dcp(individual)
    for i in xrange(len(individual)):
        if i < parametrss_limits[i][0]:
            correct_individual[i] = parametrss_limits[i][0]
        if i > parametrss_limits[i][1]:
            correct_individual[i] = parametrss_limits[i][1]
    return correct_individual

def nsga(max_generations, poblation_size, parametrss_limits, signma_sharing, initial_dummy, cross_parameter, mutation_parameter
         ,individual_creator_function, fittness_function, sharing_percentage_reduction=0.01, binary_genetics=False):
    
    Population = [individual_creator_function() for i in xrange(poblation_size)]
    BestFronts = []
    for generation in xrange(max_generations):
        classified_population = 0
        Fronts = [] # List of fronts
        FitnesValues = np.asanyarray([fittness_function(individual) for individual in Population]) # [f0,f1,f2,..] for each individual
        SharedFitnesValues = [] #Based on the front
        NonClassifiedPopulation = dcp(Population)
        front = 0
        DummyValue = initial_dummy
        while len(NonClassifiedPopulation) > 0:
            #print FitnesValues,NonClassifiedPopulation
            IND_FRONT = FrontExtraction(FitnesValues)
            #print IND_FRONT, len(FitnesValues), len(NonClassifiedPopulation)
            CURRENT_FRONT = np.take(NonClassifiedPopulation,IND_FRONT,0)
            CURRENT_FRONT_VALUES = np.take(FitnesValues,IND_FRONT,0)
            NonClassifiedPopulation = np.delete(NonClassifiedPopulation , IND_FRONT,0)
            FitnesValues = np.delete(FitnesValues , IND_FRONT, 0)
            if len(Fronts) == 0:
                BestFronts.append(CURRENT_FRONT)
            Fronts.append(IND_FRONT)
            front+=1
            #print DummyValue
            #print CURRENT_FRONT_VALUES
            SHARED_NICHE_FRONT = sharing(CURRENT_FRONT_VALUES , DummyValue , signma_sharing)
            #print SHARED_NICHE_FRONT
            SharedFitnesValues.append(SHARED_NICHE_FRONT)
            
            DummyValue = min(SHARED_NICHE_FRONT) * (1.0-sharing_percentage_reduction)
        #print "SALI!"
        ClassifiedPopulation = np.take(Population,np.concatenate(Fronts),0)  #[Population[indi] for indi in np.concatenate(Fronts)]
        #print np.concatenate(Fronts)
        #print Population
        ClassifiedPopulationRankings = np.concatenate(SharedFitnesValues)
        #print "CASS"
        #print ClassifiedPopulationRankings
        #print "CP0",ClassifiedPopulation
        #print "STOC"
        SelectedClassifiedPopulation = StochasticRemainderSelection(ClassifiedPopulationRankings, len(ClassifiedPopulationRankings))
        #print "CP1",SelectedClassifiedPopulation
        SelectedClassifiedPopulation = np.take(ClassifiedPopulation,SelectedClassifiedPopulation,0)
        #[ClassifiedPopulation[sclp] for sclp in SelectedClassifiedPopulation]
        #print "STO"
        if binary_genetics:
            #print "GEN"
            
            CrossedPopulation = CrossoverBinary(SelectedClassifiedPopulation,cross_parameter)
            MutatedPopulation = MutationBinary(CrossedPopulation, mutation_parameter)
            
        else:
            #print "NON GE"
            #print ClassifiedPopulation
            #print SelectedClassifiedPopulation
            CrossedPopulation = CrossoverBlender(SelectedClassifiedPopulation,cross_parameter)
            MutatedPopulation =[MutationRealNormal(cross_ind, mutation_parameter) for cross_ind in CrossedPopulation]
            MutatedPopulation = [apply_limits(indi,parametrss_limits) for indi in  MutatedPopulation]
            #print len(MutatedPopulation)
        Population = MutatedPopulation
    return BestFronts

#Deginimos a los individuos como un objeto, con su fitness y toa la escafandra

def test0():
    from lib.tests_nsga import t1_f1,t1_f2
    def fitness_function(Individual):
        return np.asanyarray([t1_f1(np.asanyarray([Individual]))[0],t1_f2(np.asanyarray([Individual]))[0]])

    def individual_creation_function():
        return np.random.rand(30)
    
    BEST_FRONTS = nsga(
        max_generations = 100
        ,poblation_size = 20
        ,parametrss_limits =[[0.0,1.0]]*30
        ,signma_sharing = 5.1
        ,initial_dummy = 1.0
        ,cross_parameter = 0.000000001
        ,mutation_parameter = 0.00000001
        ,individual_creator_function = individual_creation_function
        ,fittness_function = fitness_function
        ,sharing_percentage_reduction=0.01
        ,binary_genetics=False
        )
    
    FIT_FRONT = []
    for F in BEST_FRONTS:
        FIT_FRONT.append(np.asanyarray([fitness_function(R) for R in F]))
        print F
        print "---- FRENTE ---"
    FIT_FRONT = np.asanyarray(FIT_FRONT)
    for F in FIT_FRONT[-1:]:
        plt.scatter(F.T[0],F.T[1])
    plt.show()