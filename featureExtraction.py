import matplotlib.pyplot as plt
from math import log
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from ast import literal_eval
from multiprocessing import Pool
import multiprocessing
import numpy as np


def getGridRepresentation(trips_list):

    X  = []
    Y = []
    pool = Pool(multiprocessing.cpu_count())
    X = pool.map(getRoute,trips_list)
    Y = pool.map(getGTJourneyId,trips_list)
    pool.close()
    pool.join()

    return X,Y

def getRoute(trip):

    max_range = 15
    scaler = MinMaxScaler(feature_range=(0, max_range))
    data =  literal_eval(trip[1])
    scaler.fit(data)
    scaledData = scaler.transform(data)
    '''
    route = np.zeros(max_range*max_range+1)
    for point in scaledData:
        # long = x and lat = y
        y = round(point[2])
        x = round(point[1])
        # print point[1],point[2]
        # print y,x
        
        if y>0:
            # print (int)(max_range*(y-1) + x)
            route[(int)(max_range*(y-1) + x)]+=1
        else:
            # print (int)(max_range*(y) + x)
            route[(int)(max_range*(y) + x)]+=1
    '''
    route = np.zeros((max_range+1)*(max_range)+1)
    for index,point in enumerate(scaledData):
        # long = x and lat = y
        y = round(point[2])
        x = round(point[1])

        value = route[(int)(max_range*(x) + y)] + 1
        if index < (len(scaledData)-1):
            point1 = scaledData[index+1]
            y1 = round(point1[2])
            x1 = round(point1[1])
            if x1 > x and y1 > y:
                value += 1
            elif x1 > x and y1==y:
                value += 2
            elif x1 > x and y1 < y:
                value += 3
            elif x1 == x and y1 < y:
                value += 4
            elif x1 < x and y1 < y:
                value += 5
            elif x1 < x and y1 == y:
                value += 6
            elif x1 < x and y1 > y:
                value += 7
            elif x1 == x and y1 > y:
                value += 8
        route[(int)(max_range*(x) + y)] = value

    # print route
    return route


def getGTJourneyId(trip):
    return trip[0]
