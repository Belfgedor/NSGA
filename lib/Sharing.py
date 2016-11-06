import numpy as np

#front_list, the list of individual selected in the front
#dummyfitness the dummyfitness assigned to the front
#Returns a list of fitness

#Compute all the distances between each other
#It is a list which contains in the i position the j distances for i
#[[d11,d12,...d1n], [d21,d22.d]]
#
#

#a,b two realvectors 
#Output : float value (euclidean distance between a and b)
def euclidean_distance(a,b):
    return np.sqrt(np.sum((np.asanyarray(a)-np.asanyarray(b))**2))


#front_list, the list of individual selected in the front
#sharing_value -> real value (maximum phenotypic distance allowed between any two individuals)
#Output : List of floats (Niche count for each individual of the front)
def niche_count(front_list, share_value):
    NICHE_LIST = []
    for individual in front_list:
        NICHE_LIST.append(sum([1-(euclidean_distance(individual,objective)/share_value)**2 
                               if euclidean_distance(individual,objective) < share_value 
                               else 0.0 
                               for objective in front_list]))
    return np.asanyarray(NICHE_LIST)
        
    
#front_list, the list of individual selected in the front
#sharing_value -> real value (maximum phenotypic distance allowed between any two individuals)
#dummyfitness -> float (a random value or the less shared value of the last front)
def sharing( front_list, dummyfitness , share_value):
    #A Dummy Fittnes corresponds to all points in the front list
    return dummyfitness / niche_count(front_list,share_value)