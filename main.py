from preprocess import *

# df = trainDataPreprocess()
# writeToFile(df.T,"trips.csv")

clean_trips_df = clearTripleData()
writeToFile(clean_trips_df.T,"tripsClean.csv")
