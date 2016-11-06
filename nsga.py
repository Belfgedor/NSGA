import numpy as np
import matplotlib.pyplot as plt


#Deginimos a los individuos como un objeto, con su fitness y toa la escafandra

#Parameter definition
n_gen = 250.0				#Max Iterations
n_population = 100.0		#Polulation size
xover_prob = 0.8			#Crossover probability
mutation_prob = 0.01		#Mutation probability
sigma_sharing = 0.48862		#Maximum dissimilarity ( niche radius )
alpha_sharing = 1    		#sharing shape controller ( if one triangular sharing function)
n_design_var = 30.0			#Decis¡sion/Design variables

#Funtion definitions
#We consider x a (n_population * n_design_var) MATRIX
def t1_f1(population):
	return population[:,0] # return x1

def t1_g(population):
	population_aux = population[:,1:]
	sumatory = population_aux.sum(axis=1)
	return 1 + 9 * sumatory / (n_design_var-1)
def t1_h(f1,g):
	return 1 - np.sqrt(f1 / g)

def t1_f2(population):
	return t1_g(x) * t1_h(t1_f1(population),t1_g(population))