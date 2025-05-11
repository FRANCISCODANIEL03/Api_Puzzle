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

if __name__ == "__main__":
    coord = {
        'Jiloyork': (19.916012, -99.580580),
        'Toluca': (19.289165, -99.655697),
        'Atlacomulco': (19.799520, -99.873844),
        'Guadalajara': (20.677754472859146, -103.34625354877137),
        'Monterrey': (25.69161110159454, -100.321838480256),
        'QuintanaRoo': (21.163111924844458, -86.80231502121464),
        'Michohacan': (19.701400113725654, -101.20829680213464),
        'Aguascalientes': (21.87641043660486, -102.26438663286967),
        'CDMX': (19.432713075976878, -99.13318344772986),
        'QRO': (20.59719437542255, -100.38667040246602)
    }

    ruta = list(coord.keys())
    random.shuffle(ruta)

    print("Ruta inicial:", ruta)
    mejor_ruta = busqueda_tabu(ruta, coord, max_iter=500, tabu_tam=15)
    print("Mejor ruta:", mejor_ruta)
    print("Distancia incial:", evalua_ruta(ruta, coord))
    print("Distancia mejorada:", evalua_ruta(mejor_ruta, coord))
