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
	n_design_var = len(population[0])
	population_aux = population[:,1:]
	sumatory = population_aux.sum(axis=1)
	return 1 + 9.0 * sumatory / (n_design_var-1)
def t1_h(f1,g):
	return 1 - np.sqrt(f1 / g)

def t1_f2(population):
	return t1_g(population) * t1_h(t1_f1(population),t1_g(population))

def pareto_optimal_t1():
	x = np.linspace(0.0,1.0,10000)
	y = t1_h(x,1)
	plt.plot(x,y,'g')


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
	n_design_var = len(population[0])
	population_aux = population[:,1:]
	sumatory = population_aux.sum(axis=1)
	return 1 + 9.0 * sumatory / (n_design_var-1)
def t2_h(f1,g):
	return 1 - np.square(f1 / g)

def t2_f2(population):
	return t2_g(population) * t2_h(t2_f1(population),t2_g(population))

def pareto_optimal_t2():
	x = np.linspace(0.0,1.0,10000)
	y = t2_h(x,1)
	plt.plot(x,y,'g')

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
	n_design_var = len(population[0])
	population_aux = population[:,1:]
	sumatory = population_aux.sum(axis=1)
	return 1 + 9.0 * sumatory / (n_design_var-1)
def t3_h(f1,g):
	return 1 - np.sqrt(f1 / g) - (f1 / g) * np.sin(10*np.pi*f1)

def t3_f2(population):
	return t3_g(population) * t3_h(t3_f1(population),t3_g(population))

def pareto_optimal_t3():
	x = np.linspace(0.0,1.0,10000)
	y = t3_h(x,1)
	plt.plot(x,y,'g')

##################################################################

##########################  TEST 4 ################################
"""
Test Features
-------------------

Contains 21^9 LOCAL pareto-optimal fronts - test how dealing with multimodality
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
	n_design_var = len(population[0])
	population_aux = population[:,1:]
	sumatory_inside = np.square(population_aux) - 10*np.cos(4*np.pi*population_aux)
	sumatory = sumatory_inside.sum(axis=1)
	return 1 + 10.0 * (n_design_var-1) + sumatory
def t4_h(f1,g):
	return 1 - np.sqrt(f1 / g)

def t4_f2(population):
	return t4_g(population) * t4_h(t4_f1(population),t4_g(population))

def pareto_optimal_t4():
	x = np.linspace(0.0,1.0,10000)
	y = t4_h(x,1)
	plt.plot(x,y,'g')
	y = t4_h(x,1.25)
	plt.plot(x,y,'r')

##################################################################

##########################  TEST 5 ################################
"""
Test Features
-------------------

Deceptive test, where the best deceptive pareto-optimal front is g(x)=11 and the true pareto-optimal front is g(x)=10
All pareto fronts (local and global) are convex

xi_type = binary
number of decision variables: 11
x1 = {0,1}^30
x2...Xm = {0,1}^5
Pareto optimal front = g(x) = 10
deceptive pareto optimal = g(x) = 11
Population is matrix which contains the numbers of ones in each xi
"""
def v_function(unitation):
	result = []
	for ones in unitation:
		if(ones < 5):
			result.append(ones+2)
		elif(ones ==  5):
			result.append(1)
	return sum(result)


def t5_f1(population):
	return 1+population[:,0] # return x1

def t5_g(population):
	population_aux = population[:,1:]
	return np.array([v_function(x) for x in population_aux])

def t5_h(f1,g):
	return 1.0 / f1

def t5_f2(population):
	return t5_g(population) * t5_h(t5_f1(population),t5_g(population))

def pareto_optimal_t5():
	x = np.arange(1,30,1)
	y = 10 * t5_h(x,10)
	plt.plot(x,y,'g')
	y = 11 * t5_h(x,11)
	plt.plot(x,y,'r')

##################################################################

##########################  TEST 6 ################################
"""
Test Features
-------------------
Search space is non-uniform, causes 2 difficulties: pareto-optimal solutions are distributed non-uniform along the global pareto front, the front
is biases for solutions when f1(x) is close to one, the density of the solutions is lowest near the pareto-optimal front and highest away the front

NON Convex

xi_type: real 
number of decision variables: 10
xi_interval = [0,1]
Pareto optimal front = g(x) = 1

"""
def t6_f1(population):
	population_aux = population[:,0] # return x1
	sinus_power = np.power(np.sin( 6 * np.pi * population_aux), 6)
	return 1 - np.exp((-4.0) * population_aux) * sinus_power

def t6_g(population):
	n_design_var = len(population[0])
	population_aux = population[:,1:]
	sumatory = population_aux.sum(axis=1)
	return 1 + 9 * np.power( sumatory / (n_design_var-1) , 0.25)
def t6_h(f1,g):
	return 1 - np.square(f1 / g)

def t6_f2(population):
	return t6_g(population) * t6_h(t6_f1(population),t6_g(population))

def pareto_optimal_t6():
	x = np.linspace(0.0,1.0,10000)
	y = t6_h(x,1)
	plt.plot(x,y,'g')

##################################################################