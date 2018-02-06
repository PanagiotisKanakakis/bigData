import sys
from ast import literal_eval
from numpy import array, zeros, argmin, inf, equal, ndim
from scipy.spatial.distance import cdist
from utils import *
import time
import numpy as np
from collections import defaultdict
from operator import itemgetter
from multiprocessing import Pool
from functools import partial

def dtwNearestPaths(trips,test_a1):

    # parallel implementation
    trips_list = trips.values.tolist()
    for index,X in test_a1.iterrows():
        pool = Pool(4)
        routeX = literal_eval(X[0])
        start_time = time.time()
        top5 = pool.map(partial(mappedFunction, X=routeX), trips_list)
        pool.close()
        pool.join()
        top5 = sorted(top5, key=itemgetter(0))
        for i in range(0,6):
            print top5[i]
        print time.time()-start_time
        print 100*"*"

    # non parallel implementation
    # for index,X in test_a1.iterrows():
    #     routeX = literal_eval(X[0])
    #     top5 = []
    #     start_time = time.time()
    #     for index,rY in trips.iterrows():
    #         journeyPatternId = rY[0]
    #         routeY = literal_eval(rY[1])
    #         start_time = time.time()
    #         t = fastdtw(routeX,routeY)
    #         print index
    #         top5.append([t[0],journeyPatternId,time.time()-start_time])
    #         top5 = sorted(top5, key=itemgetter(0))
    #     for i in range(1,6):
    #         print top5[i]
    #     print time.time()-start_time
    #     sys.exit(0)



def mappedFunction(Y,X):
    journeyPatternId = Y[0]
    Y = literal_eval(Y[1])
    start_time = time.time()
    t = fastdtw(X,Y)
    return [t[0],journeyPatternId,time.time()-start_time]

def fastdtw(x, y, radius=1):
    return __fastdtw(x, y, radius)

def __fastdtw(x, y, radius):
    min_time_size = radius + 2

    if len(x) < min_time_size or len(y) < min_time_size:
        return dtw(x, y)

    x_shrinked = __reduce_by_half(x)
    y_shrinked = __reduce_by_half(y)
    distance, path = \
        __fastdtw(x_shrinked, y_shrinked, radius=radius)
    window = __expand_window(path, len(x), len(y), radius)
    return __dtw(x, y, window)


def dtw(x, y):
    return __dtw(x, y, None)


def __dtw(x, y, window):
    len_x, len_y = len(x), len(y)
    if window is None:
        window = [(i, j) for i in range(len_x) for j in range(len_y)]
    window = ((i + 1, j + 1) for i, j in window)
    D = defaultdict(lambda: (float('inf'),))
    D[0, 0] = (0, 0, 0)
    for i, j in window:
        dt = distanceHaversine((x[i-1][2],x[i-1][1]), (y[j-1][1],y[j-1][2]))
        D[i, j] = min((D[i-1, j][0]+dt, i-1, j), (D[i, j-1][0]+dt, i, j-1),
                      (D[i-1, j-1][0]+dt, i-1, j-1), key=lambda a: a[0])
    path = []
    i, j = len_x, len_y
    while not (i == j == 0):
        path.append((i-1, j-1))
        i, j = D[i, j][1], D[i, j][2]
    path.reverse()
    return (D[len_x, len_y][0], path)


def __reduce_by_half(x):
    # print x
    # print [(x[i] + x[1+i]) / 2 for i in range(0, len(x) - len(x) % 2, 2)]
    return [[x[i][0],(x[i][1] + x[1+i][1]) / 2,(x[i][2] + x[1+i][2]) / 2] for i in range(0, len(x) - len(x) % 2, 2)]

def __expand_window(path, len_x, len_y, radius):
    path_ = set(path)
    for i, j in path:
        for a, b in ((i + a, j + b)
                     for a in range(-radius, radius+1)
                     for b in range(-radius, radius+1)):
            path_.add((a, b))

    window_ = set()
    for i, j in path_:
        for a, b in ((i * 2, j * 2), (i * 2, j * 2 + 1),
                     (i * 2 + 1, j * 2), (i * 2 + 1, j * 2 + 1)):
            window_.add((a, b))

    window = []
    start_j = 0
    for i in range(0, len_x):
        new_start_j = None
        for j in range(start_j, len_y):
            if (i, j) in window_:
                window.append((i, j))
                if new_start_j is None:
                    new_start_j = j
            elif new_start_j is not None:
                break
        start_j = new_start_j

    return window
