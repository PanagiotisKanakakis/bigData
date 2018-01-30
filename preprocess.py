import pandas as pd
import sys
from ast import literal_eval
import geopy.distance

def trainDataPreprocess():
    df = pd.read_csv("train_set.csv").dropna()

    init = df.head(n=1)
    for index, row in init.iterrows():
        init_row = row

    id = 0
    dict = {}
    points = []
    for index, row in df.iterrows():
        if(init_row['journeyPatternId'] == row['journeyPatternId']):
            points.append( [ row['timestamp'],row['latitude'],row['longitude'] ] )
        else:
            dict[id] = [init_row['journeyPatternId'] , init_row['vehicleID'],points]
            points = []
            points.append( [ row['timestamp'],row['latitude'],row['longitude'] ] )
            init_row = row
            id+=1

    return pd.DataFrame.from_dict(dict)

def writeToFile(df,filename):
    df.to_csv(filename)
    return


def clearTripleData():
    df = pd.read_csv("trips.csv")
    # count total routes. last index value
    totalRoutes = df.tail(1).index.item()

    dict = {}
    totalDistanceCriteria = 0
    maxDistanceCriteria = 0
    for r in df.iterrows():
        row = r[1]
        route = literal_eval(row[2])
        if len(route) > 2:
            totalRouteDistance,pruneFromData = calculateTotalRouteDistance(route)
            if totalRouteDistance < 2.0 or pruneFromData:
                if pruneFromData:
                    # max distance filter
                    maxDistanceCriteria +=1
                else:
                    # total distance filter
                    totalDistanceCriteria +=1
            else:
                dict[r[0]] = row


    print "Total routes are " + str(totalRoutes)
    print "Routes deleted by the total distance filter " + str(totalDistanceCriteria)
    print "Routes deleted by the max distance filter " + str(maxDistanceCriteria)
    print "Updated data contains  " + str(len(dict)) + " records!"
    return pd.DataFrame.from_dict(dict)

def calculateTotalRouteDistance(route):

    totalDistance = 0
    pruneFromData = False
    for i in range(0,len(route)-1):
        point1 = (route[i][1],route[i][2])
        point2 = (route[i+1][1],route[i+1][2])
        distance = distanceCount(point1,point2)
        if distance > 2.0:
            # max distance between two points bigger than 2km.
            # record should be removed from data
            pruneFromData = True
        totalDistance += distance
    return totalDistance,pruneFromData

def distanceCount(point1,point2):
    return geopy.distance.vincenty(point1,point2).km
