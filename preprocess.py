import pandas as pd
import sys
from ast import literal_eval
import geopy.distance
from utils import *

def trainDataPreprocess():
    df = pd.read_csv("train_set.csv").dropna()
    id = 0
    dict = {}
    dict2 = {}

    for index, row in df.iterrows():
        if row['vehicleID'] in dict2 and row['journeyPatternId'] == dict2[row['vehicleID']][0]:
            dict[dict2[row['vehicleID']][1]][1].append( [ row['timestamp'],row['longitude'],row['latitude'] ] )
        else:
            dict[id] = [row['journeyPatternId'], [[row['timestamp'],row['longitude'],row['latitude']]] ]
            dict2[row['vehicleID']] = [row['journeyPatternId'], id]
            id+=1


    return pd.DataFrame.from_dict(dict)

def clearTripleData():
    df = pd.read_csv("trips.csv",usecols=["0", "1"])
    # count total routes. last index value
    totalRoutes = df.tail(1).index.item()
    dict = {}
    totalDistanceCriteria = 0
    maxDistanceCriteria = 0
    for index,r in df.iterrows():
        route = literal_eval(r[1])
        if len(route) >= 2:
            totalRouteDistance,pruneFromData = calculateTotalRouteDistance(route)
            if totalRouteDistance < 2.0 or pruneFromData:
                if pruneFromData:
                    # max distance filter
                    maxDistanceCriteria +=1
                else:
                    # total distance filter
                    totalDistanceCriteria +=1
            else:
                dict[index] = r
        else:
            totalDistanceCriteria +=1
    print "Total routes are " + str(totalRoutes+1)
    print "Routes deleted by the total distance filter " + str(totalDistanceCriteria)
    print "Routes deleted by the max distance filter " + str(maxDistanceCriteria)
    print "Updated data contains  " + str(len(dict)) + " records!"
    return pd.DataFrame.from_dict(dict)

def calculateTotalRouteDistance(route):

    totalDistance = 0
    pruneFromData = False
    for i in range(0,len(route)-1):
        point1 = (route[i][2],route[i][1])
        point2 = (route[i+1][2],route[i+1][1])
        distance = distanceHaversine(point1,point2)
        if distance > 2.0:
            # max distance between two points bigger than 2km.
            # record should be removed from data
            pruneFromData = True
        totalDistance += distance
    return totalDistance,pruneFromData

def plotFiveRandomCleanTrips():
    df = pd.read_csv("tripsClean.csv",usecols=["Unnamed: 0", "0", "1"])
    df_random = df.sample(n=5)
    for index,r in df_random.iterrows():
        route = literal_eval(r[2])
        plot(route, "./plots/tripID:"+str(r[0])+"_JourID:"+r[1])
