import math
import random
import networkx as nx
import matplotlib.pyplot as plt

def distancia(coord1, coord2):
    lat1, long1 = coord1
    lat2, long2 = coord2
    return math.sqrt((lat1 - lat2) ** 2 + (long1 - long2) ** 2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    return total 

def generar_vecinos(ruta):
    vecinos = []
    for i in range(len(ruta)):
        for j in range(i + 1, len(ruta)):
            vecino = ruta[:]
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append((vecino, (ruta[i], ruta[j])))
    return vecinos

def es_tabu(movimiento, memoria_tabu):
    a, b = movimiento
    return f"{a}_{b}" in memoria_tabu or f"{b}_{a}" in memoria_tabu

def actualizar_memoria(memoria_tabu):
    eliminar = []
    for key in memoria_tabu:
        memoria_tabu[key] -= 1
        if memoria_tabu[key] <= 0:
            eliminar.append(key)
    for key in eliminar:
        del memoria_tabu[key]

def busqueda_tabu(ruta_inicial, coord, iteraciones=100, persistencia=5):
    mejor_ruta = ruta_inicial[:]
    mejor_distancia = evalua_ruta(mejor_ruta, coord)
    memoria_tabu = {}

    ruta_actual = ruta_inicial[:]

    for _ in range(iteraciones):
        vecinos = generar_vecinos(ruta_actual)
        vecinos.sort(key=lambda x: evalua_ruta(x[0], coord))

        for vecino, movimiento in vecinos:
            if not es_tabu(movimiento, memoria_tabu) or evalua_ruta(vecino, coord) < mejor_distancia:
                ruta_actual = vecino[:]
                distancia_actual = evalua_ruta(ruta_actual, coord)
                if distancia_actual < mejor_distancia:
                    mejor_ruta = ruta_actual[:]
                    mejor_distancia = distancia_actual
                memoria_tabu[f"{movimiento[0]}_{movimiento[1]}"] = persistencia
                break

        actualizar_memoria(memoria_tabu)

    return mejor_ruta
