import pandas as pd
import math

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
