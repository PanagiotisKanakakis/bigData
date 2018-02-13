import time
from operator import itemgetter
from numpy import array, zeros, argmin, inf, equal, ndim
import numpy as np
from collections import defaultdict
from multiprocessing import Pool
import multiprocessing
from functools import partial
from utils import *

def lcss(trips,test_a2):
    # parallel implementation
    trips_list = trips.values.tolist()
    for index,X in test_a2.iterrows():
        routeX = literal_eval(X[0])
        
        start_time = time.time()
        pool = Pool(multiprocessing.cpu_count())
        top5 = pool.map(partial(mappedFunction, X=routeX), trips_list)
        pool.close()
        pool.join()
        top5 = sorted(top5, key=itemgetter(0), reverse=True)
        
        plot(routeX, "./plots/lcss/"+str(index)+"/lcss_route_"+str(index))
        
        for i in range(0,6):
            print "Neighbour "+str(i)+": matched="+ str(top5[i][0]) + "  -  journayId=" + top5[i][1] + "  -  time=" + str(top5[i][2])
            plotLCSS(top5[i][3], top5[i][4], "./plots/lcss/"+str(index)+"/lcss_neighbour_"+str(i)+"_for_route_"+str(index))
        print "Total time = "+str(time.time()-start_time)
        print 100*"*"
        
    '''
    # non parallel implementation
    for index,X in test_a2.iterrows():
        routeX = literal_eval(X[0])
        top5 = []
        start_time = time.time()
        for index,rY in trips.iterrows():
            journeyPatternId = rY[0]
            routeY = literal_eval(rY[1])
            
            t = lcsRos(routeX, routeY)
            
            top5.append([len(t),journeyPatternId,time.time()-start_time])
            top5 = sorted(top5, key=itemgetter(0), reverse=True)
        print time.time()-start_time
        for i in range(0,6):
            print top5[i]
    '''
    
def mappedFunction(Y,X):
    journeyPatternId = Y[0]
    Y = literal_eval(Y[1])
    start_time = time.time()
    t = lcsRos(X, Y)
    return [len(t),journeyPatternId,time.time()-start_time,Y, t]

def checkIfClose(X, Y):
    dt = distanceHaversine((X[2],X[1]), (Y[2],Y[1]))
    return dt*1000 <= 200

def lcsRos(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if checkIfClose(x, y):
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = []
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert checkIfClose(a[x-1],b[y-1])
            result = [b[y-1]] + result
            x -= 1
            y -= 1
    return result
