import numpy as np
import matplotlib.pyplot as plt
from lib.Crossover import CrossoverBinary,CrossoverBlender
from lib.ExtractFront import FrontExtraction
from lib.Mutation import MutationBinary,MutationRealNormal
from lib.SRS import StochasticRemainderSelection
from lib.Sharing import sharing
from copy import deepcopy as dcp
import matplotlib.cm as cm
import itertools

#import lib.tests_nsga as TESTS

def hyper_volumen_indicator(front_values,limits):
    sorted_front = np.asanyarray(np.sort(front_values,axis=0))
    area_accum = 0
    for first_point in xrange(len(sorted_front)-1):
        second_point = first_point + 1
        fpx = sorted_front[first_point][0]
        fpy = sorted_front[first_point][1]
        spx = sorted_front[second_point][0]
        spy = sorted_front[second_point][1]
        base = spx - fpx
        height = limits[1] - fpy
        area_accum += base * height

    #when finished only last point lasts
    last_point = sorted_front[-1]# take the last point
    lpx = last_point[0]
    lpy = last_point[1]
    base = limits[0] - lpx
    height = limits[1] - lpy
    area_accum += base * height
    return area_accum

def apply_limits(individual,parametrss_limits):
    correct_individual = dcp(individual)
    for i in xrange(len(individual)):
        if individual[i] < parametrss_limits[i][0]:
            correct_individual[i] = parametrss_limits[i][0]
        if individual[i] > parametrss_limits[i][1]:
            correct_individual[i] = parametrss_limits[i][1]
    return correct_individual

def nsga(max_generations, poblation_size, parametrss_limits, signma_sharing, initial_dummy, cross_parameter, mutation_parameter
         ,individual_creator_function, fittness_function, hiperplane_limits=None, pareto_fron_func=None, sharing_percentage_reduction=0.01, binary_genetics=False, Name="GA"):
    
    Population = [individual_creator_function() for i in xrange(poblation_size)]
    BestFronts = []
    HiperFronts = []
    for generation in xrange(max_generations):
        classified_population = 0
        #print generation    
        Fronts = [] # List of fronts
        FitnesValues = np.asanyarray([fittness_function(individual) for individual in Population]) # [f0,f1,f2,..] for each individual
        #print "POB",Population
        #print "FV:",FitnesValues
        
        
        SharedFitnesValues = [] #Based on the front
        NonClassifiedPopulation = dcp(Population)
        front = 0
        DummyValue = initial_dummy
        colors = iter(cm.rainbow(np.linspace(0, 5, 100)))
        #itertools.cycle(["r", "b", "g", "c", "m","y","k"])
        while len(NonClassifiedPopulation) > 0:
            #print FitnesValues,NonClassifiedPopulation
            IND_FRONT = FrontExtraction(FitnesValues)
            
            #print IND_FRONT, len(FitnesValues), len(NonClassifiedPopulation)
            CURRENT_FRONT = np.take(NonClassifiedPopulation,IND_FRONT,0)
            CURRENT_FRONT_VALUES = np.take(FitnesValues,IND_FRONT,0)
            #print "CF",CURRENT_FRONT_VALUES
            
            NonClassifiedPopulation = np.delete(NonClassifiedPopulation , IND_FRONT,0)
            FitnesValues = np.delete(FitnesValues , IND_FRONT, 0)
            if len(Fronts) == 0:
                BestFronts.append(CURRENT_FRONT)
                if hiperplane_limits != None : 
                    HiperFronts.append(hyper_volumen_indicator(CURRENT_FRONT_VALUES,hiperplane_limits))
                    
            if (10 == generation ) or (max_generations/2 == generation ) or generation == max_generations-1 :
                    #print generation, generation %10
                    #print front,"--------------------------"
                    #print CURRENT_FRONT_VALUES
                    plt.scatter(CURRENT_FRONT_VALUES.T[0],CURRENT_FRONT_VALUES.T[1], color=next(colors))
                    
            Fronts.append(IND_FRONT)
            front+=1
            #print DummyValue
            #print CURRENT_FRONT_VALUES
            
            SHARED_NICHE_FRONT = sharing(CURRENT_FRONT_VALUES , DummyValue , signma_sharing)
            #print "niche"
            #print SHARED_NICHE_FRONT
            #print SHARED_NICHE_FRONT
            SharedFitnesValues.append(SHARED_NICHE_FRONT)
            try:
                pass
                DummyValue = min(SHARED_NICHE_FRONT) * (1.0-sharing_percentage_reduction)
            except Exception as e:
                print e
                print FitnesValues,NonClassifiedPopulation
                print SHARED_NICHE_FRONT
                return 0
            
        if (10 == generation ) or (max_generations/2 == generation ) or generation == max_generations-1 :
            if pareto_fron_func != None: pareto_fron_func()
            plt.title("Generacion " + str(generation) + " Ferentes : " + str(len(Fronts)) )
            plt.savefig(Name +"_"+str(generation)+'.png')
            plt.show()
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
        #print "SELP",SelectedClassifiedPopulation
        #print "STO"
        if binary_genetics:
            #print "GEN"
            
            CrossedPopulation = CrossoverBinary(SelectedClassifiedPopulation,cross_parameter)
            MutatedPopulation = [MutationBinary(cross_ind, mutation_parameter) for cross_ind in CrossedPopulation]
            
        else:
            #print "NON GE"
            #print ClassifiedPopulation
            #print SelectedClassifiedPopulation
            CrossedPopulation = CrossoverBlender(SelectedClassifiedPopulation,cross_parameter)
            #print "CROS POP:",CrossedPopulation
            MutatedPopulation =[MutationRealNormal(cross_ind, mutation_parameter) for cross_ind in CrossedPopulation]
            #print "MUT POB:",MutatedPopulation
            MutatedPopulation = [apply_limits(indi,parametrss_limits) for indi in  MutatedPopulation]
            #print "MUT REG :",MutatedPopulation
            #print len(MutatedPopulation)
        Population = MutatedPopulation
    if len(HiperFronts) != 0:
        plt.plot(HiperFronts)
        plt.title("Hipervolume Evolution in the first front")
        plt.savefig(Name +"_Hiper_"+str(generation)+'.png')
        plt.show()
    return BestFronts

#Deginimos a los individuos como un objeto, con su fitness y toa la escafandra


def fitness_function_1(Individual):
    return np.asanyarray([t1_f1(np.asanyarray([Individual]))[0],t1_f2(np.asanyarray([Individual]))[0]])

def fitness_function_2(Individual):
    return np.asanyarray([t2_f1(np.asanyarray([Individual]))[0],t2_f2(np.asanyarray([Individual]))[0]])

def fitness_function_3(Individual):
    return np.asanyarray([t3_f1(np.asanyarray([Individual]))[0],t3_f2(np.asanyarray([Individual]))[0]])


def fitness_function_4(Individual):
    return np.asanyarray([t4_f1(np.asanyarray([Individual]))[0],t4_f2(np.asanyarray([Individual]))[0]])

def fitness_function_5(Individual):
    IndiTrans = [sum(x) for x in Individual]
    return np.asanyarray([t5_f1(np.asanyarray([IndiTrans]))[0],t5_f2(np.asanyarray([IndiTrans]))[0]])

def fitness_function_6(Individual):
    return np.asanyarray([t6_f1(np.asanyarray([Individual]))[0],t6_f2(np.asanyarray([Individual]))[0]])


def individual_creation_function_1():
    return np.random.rand(30)

def individual_creation_function_4():
    return np.concatenate([np.random.rand(1),np.random.rand(9)*10 -5])

def individual_creation_function_6():
    return np.random.rand(10)


def individual_creation_function_5():
    return (MutationBinary([[0]*30] + [[0]*5]*10,0.5))


BEST_FRONTS = nsga(
    max_generations = 250
    ,poblation_size = 100
    ,parametrss_limits = [[0.0,1.0]]*30
    ,signma_sharing = 0.48862 
    ,initial_dummy = 100.0
    ,cross_parameter = 0.8
    ,mutation_parameter = 0.01
    ,individual_creator_function = individual_creation_function_1
    ,fittness_function = fitness_function_1
    ,pareto_fron_func=pareto_optimal_t1
    ,hiperplane_limits=np.asanyarray([1,2])
    ,sharing_percentage_reduction=0.0001
    ,binary_genetics=False
    ,Name="Test1"
)

BEST_FRONTS = nsga(
    max_generations = 250
    ,poblation_size = 100
    ,parametrss_limits = [[0.0,1.0]]*30
    ,signma_sharing = 0.48862 
    ,initial_dummy = 100.0
    ,cross_parameter = 0.8
    ,mutation_parameter = 0.01
    ,individual_creator_function = individual_creation_function_1
    ,fittness_function = fitness_function_2
    ,pareto_fron_func= pareto_optimal_t2
    ,hiperplane_limits=np.asanyarray([1,2])
    ,sharing_percentage_reduction=0.0001
    ,binary_genetics=False
    ,Name="Test2"
)

BEST_FRONTS = nsga(
    max_generations = 250
    ,poblation_size = 100
    ,parametrss_limits = [[0.0,1.0]]*30
    ,signma_sharing = 0.48862 
    ,initial_dummy = 100.0
    ,cross_parameter = 0.8
    ,mutation_parameter = 0.01
    ,individual_creator_function = individual_creation_function_1
    ,fittness_function = fitness_function_3
    ,pareto_fron_func= pareto_optimal_t3
    ,hiperplane_limits=np.asanyarray([1,2])
    ,sharing_percentage_reduction=0.0001
    ,binary_genetics=False
    ,Name="Test3"
)

BEST_FRONTS = nsga(
    max_generations = 250
    ,poblation_size = 100
    ,parametrss_limits = [[0.0,1.0]]+[[0.0,5.0]]*9
    ,signma_sharing = 0.48862 
    ,initial_dummy = 100.0
    ,cross_parameter = 0.8
    ,mutation_parameter = 0.01
    ,individual_creator_function = individual_creation_function_4
    ,fittness_function = fitness_function_4
    ,pareto_fron_func= pareto_optimal_t4
    ,hiperplane_limits=np.asanyarray([1,2])
    ,sharing_percentage_reduction=0.0001
    ,binary_genetics=False
    ,Name="Test4"
)


BEST_FRONTS = nsga(
    max_generations = 250
    ,poblation_size = 100
    ,parametrss_limits = None
    ,signma_sharing = 34
    ,initial_dummy = 100.0
    ,cross_parameter = 0.8
    ,mutation_parameter = 0.01
    ,individual_creator_function = individual_creation_function_5
    ,fittness_function = fitness_function_5
    ,pareto_fron_func= pareto_optimal_t5
    ,hiperplane_limits=np.asanyarray([31,100])
    ,sharing_percentage_reduction=0.0001
    ,binary_genetics=True
    ,Name="Test5"
)

BEST_FRONTS = nsga(
    max_generations = 250
    ,poblation_size = 100
    ,parametrss_limits = [[0.0,1.0]]*10
    ,signma_sharing = 0.48862 
    ,initial_dummy = 100.0
    ,cross_parameter = 0.8
    ,mutation_parameter = 0.01
    ,individual_creator_function = individual_creation_function_6
    ,fittness_function = fitness_function_6
    ,pareto_fron_func= pareto_optimal_t6
    ,hiperplane_limits=np.asanyarray([1,5])
    ,sharing_percentage_reduction=0.0001
    ,binary_genetics=False
    ,Name="Test6"
)
