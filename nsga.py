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

#Here goes the main code
