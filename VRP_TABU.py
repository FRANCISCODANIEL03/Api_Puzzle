import math
import random
from operator import itemgetter
from copy import deepcopy

# ------------------------- Funciones auxiliares -------------------------

def distancia(coord1, coord2):
    lat1, long1 = coord1
    lat2, long2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (long1 - long2)**2)

def peso_ruta(ruta, pedidos):
    return sum(pedidos[c] for c in ruta)
