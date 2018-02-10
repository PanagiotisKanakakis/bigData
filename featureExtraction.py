import matplotlib.pyplot as plt
from math import log
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from ast import literal_eval
from multiprocessing import Pool
import multiprocessing
import numpy as np


def getGridRepresentation(filename):

    df_tripsClean = pd.read_csv(filename,usecols=["0", "1", "2"])
    trips_list = df_tripsClean.values.tolist()

    X  = []
    Y = []
    pool = Pool(multiprocessing.cpu_count())
    X = pool.map(getRoute,trips_list)
    Y = pool.map(getGTJourneyId,trips_list)
    pool.close()
    pool.join()

    return X,Y

def getRoute(trip):

    scaler = MinMaxScaler(feature_range=(0, 1))
    data =  literal_eval(trip[2])
    scaler.fit(data)
    scaledData = scaler.transform(data)

    route = np.zeros(100)
    for point in scaledData:
        # long = x and lat = y
        y = point[1]
        x = point[2]
        route[(int)(10*x + y)]+=1

    return route


def getGTJourneyId(trip):
    return trip[0]
