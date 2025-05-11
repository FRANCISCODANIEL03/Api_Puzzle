import math
import random
from collections import deque

def distancia(coord1, coord2):
    lat1 = coord1[0]
    long1 = coord1[1]
    lat2 = coord2[0]
    long2 = coord2[1]
    return math.sqrt((lat1 - lat2) ** 2 + (long1 - long2) ** 2)
