from preprocess import *
from utils import *
from dtw import *
from lcss import *
from featureExtraction import *
from classification import *
#from nltk import ngrams

df = trainDataPreprocess()
writeToFile(df.T,"trips.csv")

clean_trips_df = clearTripleData()
writeToFile(clean_trips_df.T,"tripsClean.csv")

plotFiveRandomCleanTrips()

trips , test_a1 = generateSequences("tripsClean.csv" , "test_set_a1.csv")
dtwNearestPaths(trips,test_a1)

trips , test_a2 = generateSequences("tripsClean.csv" , "test_set_a2.csv")
lcss(trips, test_a2)

X,Y = getGridRepresentation(getTripsCleanAsList("tripsClean.csv"))
evaluationMetrics(X,Y)
