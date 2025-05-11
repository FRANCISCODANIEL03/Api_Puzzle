import math
import random
from collections import deque

def distancia(coord1, coord2):
    lat1 = coord1[0]
    long1 = coord1[1]
    lat2 = coord2[0]
    long2 = coord2[1]
    return math.sqrt((lat1 - lat2) ** 2 + (long1 - long2) ** 2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])  # volver al inicio
    return total

def generar_vecinos(ruta):
    vecinos = []
    for i in range(len(ruta)):
        for j in range(i + 1, len(ruta)):
            vecino = ruta[:]
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append((vecino, (ruta[i], ruta[j])))
    return vecinos

def busqueda_tabu(ruta_inicial, coord, max_iter=100, tabu_tam=10):
    mejor_ruta = ruta_inicial[:]
    mejor_costo = evalua_ruta(mejor_ruta, coord)
    ruta_actual = mejor_ruta[:]
    tabu = deque(maxlen=tabu_tam)

    for _ in range(max_iter):
        vecinos = generar_vecinos(ruta_actual)
        mejor_vecino = None
        mejor_vecino_costo = float('inf')
        mejor_movimiento = None

        for vecino, movimiento in vecinos:
            if movimiento in tabu or (movimiento[1], movimiento[0]) in tabu:
                continue

            costo = evalua_ruta(vecino, coord)
            if costo < mejor_vecino_costo:
                mejor_vecino = vecino
                mejor_vecino_costo = costo
                mejor_movimiento = movimiento

        if mejor_vecino is None:
            break  # No se encontraron vecinos válidos

        ruta_actual = mejor_vecino[:]
        tabu.append(mejor_movimiento)

        if mejor_vecino_costo < mejor_costo:
            mejor_ruta = mejor_vecino[:]
            mejor_costo = mejor_vecino_costo

    return mejor_ruta
