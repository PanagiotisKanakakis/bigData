from preprocess import *
from utils import *
from dtw import *
from featureExtraction import *


# df = trainDataPreprocess()
# writeToFile(df.T,"trips.csv")
#
# clean_trips_df = clearTripleData()
# writeToFile(clean_trips_df.T,"tripsClean.csv")
#
# trips , test_a1 = generateSequences("tripsClean.csv" , "test_set_a1.csv")
# dtwNearestPaths(trips,test_a1)

X,Y = getGridRepresentation("tripsClean.csv")
