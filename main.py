from preprocess import *
from utils import *
from dtw import *
from lcss import *
from featureExtraction import *
from classification import *
from nltk import ngrams

#df = trainDataPreprocess()
#writeToFile(df.T,"trips.csv")
#
#clean_trips_df = clearTripleData()
#writeToFile(clean_trips_df.T,"tripsClean.csv")
#

#plotFiveRandomCleanTrips()

#trips , test_a1 = generateSequences("tripsClean.csv" , "test_set_a1.csv")
#dtwNearestPaths(trips,test_a1)

#trips , test_a2 = generateSequences("tripsClean.csv" , "test_set_a2.csv")
#lcss(trips, test_a2)

X,Y = getGridRepresentation(getTripsCleanAsList("tripsClean.csv"))
'''
X = [array([1., 2., 3.]), array([4., 5., 6.])]
n = 2
array1 = []
for x in X:
    twograms = ngrams(x, n)
    array = []
    for grams in twograms:
    #for grams in x:
        #print grams
        array.append(str(grams[0])+"-"+str(grams[1]))
        #array.append(grams)
        #print array
    #print array
    #flat_list = [item for sublist in array for item in sublist]
    array1.append(array)
#print array1
'''
'''
#X = [array([1., 2., 3.]), array([4., 5., 6.])]
n = 2
array1 = []
a1 = []
for x in X:
    twograms = ngrams(x, n)
    array = []
    a2 = []
    for grams in twograms:
        array.append(grams)
    #print array
    for index,i in enumerate(x):
        if index < len(array):
            t  = array[index]
            if t[0] < t[1]:
                i = i+1.0
        a2.append(i)
    a1.append(a2)   
#print a1
'''
evaluationMetrics(X,Y)
