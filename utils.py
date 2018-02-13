import pandas as pd
import math
import gmplot
from ast import literal_eval

def getTripsCleanAsList(filename):
    # df_tripsClean = pd.read_csv(filename,usecols=["0", "1", "2"])
    df_tripsClean = pd.read_csv(filename,usecols=["0","2"])
    return df_tripsClean.values.tolist()

def writeToFile(df,filename):
    df.to_csv(filename)
    return

def generateSequences(trips,filename):
    fields = ['0', '2']
    df_trips = pd.read_csv(trips, usecols=fields)
    df_test = pd.read_csv(filename,sep='\n')
    return df_trips,df_test

def distanceHaversine(point1,point2):

    lat1 = point1[0]
    lon1 = point1[1]

    lat2 = point2[0]
    lon2 = point2[1]

    R = 6371 # km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat/2.0) * math.sin(dLat/2.0) + math.sin(dLon/2.0) * math.sin(dLon/2.0) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c

    # y = math.sin(dLon) * math.cos(lat2)
    # x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon)
    # brng = math.atan2(y,x)
    # print d,(brng/(2*math.pi))*360
    # return d,(brng/(2*math.pi))*360
    return d

def plot(df):
    for index,r in df.iterrows():
        route = literal_eval(r[2])
        gmap = gmplot.GoogleMapPlotter(route[len(route)/2][1],route[len(route)/2][2], 13)
        longitudes = [x[1] for x in route]
        latitudes  = [x[2] for x in route]
        gmap.plot(longitudes, latitudes, 'green', edge_width=4)
        gmap.draw("./plots/tripID:"+`r[0]`+"_JourID:"+r[1]+".html")
