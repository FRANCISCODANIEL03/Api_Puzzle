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

def clientes_en_ruta(ruta):
    return len(ruta)

def esta_restringido(ciudad1, ciudad2, restricciones):
    return (ciudad1, ciudad2) in restricciones or (ciudad2, ciudad1) in restricciones

def distancia_total(rutas, coord, almacen):
    total = 0
    for ruta in rutas:
        if ruta:
            total += distancia(almacen, coord[ruta[0]])  # del almacén al primero
            for i in range(len(ruta) - 1):
                total += distancia(coord[ruta[i]], coord[ruta[i+1]])
            total += distancia(coord[ruta[-1]], almacen)  # del último al almacén
    return total

def es_factible(rutas, pedidos, max_carga, max_clientes, restricciones):
    for ruta in rutas:
        if peso_ruta(ruta, pedidos) > max_carga or clientes_en_ruta(ruta) > max_clientes:
            return False
        for i in range(len(ruta) - 1):
            if esta_restringido(ruta[i], ruta[i+1], restricciones):
                return False
    return True

