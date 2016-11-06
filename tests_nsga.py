import numpy as np
import matplotlib.pyplot as plt

#Funtion definitions
#We consider x a (n_population * n_design_var) MATRIX
##########################  TEST 1 ################################
"""
Test Features
-------------------

Convex pareto optimal front

xi_type = real
number of decision variables: 30
xi_interval = [0,1]
Pareto optimal front = g(x) = 1

"""
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

##################################################################

##########################  TEST 2 ################################
"""
Test Features
-------------------
non-convex pareto optimal front

xi_type = real 
number of decision variables: 30
xi_interval = [0,1]
Pareto optimal front = g(x) = 1

"""
def t2_f1(population):
	return population[:,0] # return x1

def t2_g(population):
	population_aux = population[:,1:]
	sumatory = population_aux.sum(axis=1)
	return 1 + 9 * sumatory / (n_design_var-1)
def t2_h(f1,g):
	return 1 - np.square(f1 / g)

def t2_f2(population):
	return t2_g(x) * t2_h(t2_f1(population),t2_g(population))

##################################################################

##########################  TEST 3 ################################
"""
Test Features
--------------

Non-contiguous convex parts, test the discreteness pareto optimal front
No discontinuity in the parameter space

xi_type = real
number of decision variables: 30
xi_interval = [0,1]
Pareto optimal front = g(x) = 1

"""
def t3_f1(population):
	return population[:,0] # return x1

def t3_g(population):
	population_aux = population[:,1:]
	sumatory = population_aux.sum(axis=1)
	return 1 + 9 * sumatory / (n_design_var-1)
def t3_h(f1,g):
	return 1 - np.sqrt(f1 / g) - (f1 / g) * np.sin(10*np.pi*f1)

def t3_f2(population):
	return t3_g(x) * t3_h(t3_f1(population),t3_g(population))

##################################################################

##########################  TEST 4 ################################
"""
Test Features
-------------------

Contains 21⁹ LOCAL pareto-optimal fronts - test how dealing with multimodality
How its able to reach the global optimal front

xi_type = real
number of decision variables: 10
x1_interval = [0,1]
X2...Xm interval = [-5,5]
Pareto optimal front = g(x) = 1
Best - LOCAL pareto optimal front = g(x) = 1.25

"""
def t4_f1(population):
	return population[:,0] # return x1

def t4_g(population):
	population_aux = population[:,1:]
	sumatory_inside = np.square(population_aux) - 10*np.cos(4*np.pi*population_aux)
	sumatory = sumatory_inside.sum(axis=1)
	return 1 + 10 * (n_design_var-1) + sumatory
def t4_h(f1,g):
	return 1 - np.sqrt(f1 / g)

def t4_f2(population):
	return t4_g(x) * t4_h(t4_f1(population),t4_g(population))

##################################################################

##########################  TEST 5 ################################
"""
Test Features
-------------------

Deceptive test, where the best deceptive pareto-optimal front is g(x)=11 and the true pareto-optimal front is g(x)=10
All pareto fronts (local and global) are convex

xi_type = binary
number of decision variables: 11
x1 = {0,1}³⁰ 
x2...Xm = {0,1}⁵
Pareto optimal front = g(x) = 1

"""
def unitation(x1):
	return x1.sum(axis=1)
	
def t5_f1(population):
	return population[:,0] # return x1

def t5_g(population):
	population_aux = population[:,1:]
	sumatory = population_aux.sum(axis=1)
	return 1 + 9 * sumatory / (n_design_var-1)
def t5_h(f1,g):
	return 1 - np.sqrt(f1 / g)

def t5_f2(population):
	return t5_g(x) * t5_h(t5_f1(population),t5_g(population))

##################################################################

##########################  TEST 1 ################################
"""
Test Features
-------------------

number of decision variables:
xi_interval = [0,1]
Pareto optimal front = g(x) = 1

"""
def t6_f1(population):
	return population[:,0] # return x1

def t6_g(population):
	population_aux = population[:,1:]
	sumatory = population_aux.sum(axis=1)
	return 1 + 9 * sumatory / (n_design_var-1)
def t6_h(f1,g):
	return 1 - np.sqrt(f1 / g)

def t6_f2(population):
	return t6_g(x) * t6_h(t6_f1(population),t6_g(population))

##################################################################