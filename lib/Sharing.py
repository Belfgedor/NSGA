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
    result = np.sqrt(np.sum((np.asanyarray(a)-np.asanyarray(b))**2))


    print result
    return result


def share(Individual, objective, share_value, alpha=2):
    if euclidean_distance(Individual,objective) < share_value:
        return 1-(euclidean_distance(Individual,objective)/share_value)**alpha  
    else: 
        return 0.0 

#front_list, the list of individual selected in the front
#sharing_value -> real value (maximum phenotypic distance allowed between any two individuals)
#Output : List of floats (Niche count for each individual of the front)
def niche_count(front_list, share_value, alpha=2):
    NICHE_LIST = []
    for indi in xrange(len(front_list)):
        NICHE_LI = [share(front_list[indi], front_list[obj], share_value, alpha=2) if obj != indi else 0 for obj in xrange(len(front_list))]
        #print "NICHE _ VAl ",NICHE_LI
        NICHE_LIST.append(np.sum(NICHE_LI))
    return np.asanyarray(NICHE_LIST)
    
#front_list, the list of individual selected in the front
#sharing_value -> real value (maximum phenotypic distance allowed between any two individuals)
#dummyfitness -> float (a random value or the less shared value of the last front)
def sharing( front_list, dummyfitness , share_value, alpha=2):
    #A Dummy Fittnes corresponds to all points in the front list
    nc =niche_count(front_list,share_value, alpha=2)
    #nc = np.delete(nc,np.where(nc == 0)[0])
    #np.where(nc == 0)[0]
    return np.asanyarray( [(dummyfitness /  c) if c != 0 else 0.000000001  for c in nc]  )  #niche_count(front_list,share_value, alpha=2)