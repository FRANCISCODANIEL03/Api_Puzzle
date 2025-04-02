#VRP con restricciones adicionales
import math 
from operator import itemgetter

# ------------------------- Funciones auxiliares -------------------------

def distancia(coord1, coord2):
    lat1, long1 = coord1
    lat2, long2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (long1 - long2)**2)

def en_ruta(rutas, ciudad):
    for r in rutas:
        if ciudad in r:
            return r
    return None
