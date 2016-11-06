import numpy as np

#front_list, the list of individual selected in the front
#dummyfitness the dummyfitness assigned to the front
#Returns a list of fitness

#Compute all the distances between each other
#It is a list which contains in the i position the j distances for i
#[[d11,d12,...d1n], [d21,d22.d]]
#
#
def euclidean_distance(vector1,vector2):
	result = 0
	for i in xrange(len(vector1)):
		result += np.square(vector2[i]-vector1[i])
	return np.sqrt(result)
def compute_distances():


def niche_count(individual):
	distances = compute_distances();
	sum(share_function())

def sharing( front_list, dummyfitness ):
	return [dummyfitness / niche_count(individual) for individual in front_list]

