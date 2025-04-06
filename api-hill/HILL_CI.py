# TSP con Hill Climbing Iterativo
import math
import random

def distancia(coord1, coord2):
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

# Calcular la distancia correcta por una ruta
def evalua_ruta(ruta):
    total = 0
    for i in range(0, len(ruta)-1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total = total + distancia(coord[ciudad1], coord[ciudad2])
    ciudad1 = ruta[i + 1]
    ciudad2 = ruta[0]
    total = total + distancia(coord[ciudad1], coord[ciudad2])
    return total

def i_hill_climbing(coord):
    # Crear ruta inicial aleatoria
    ruta = []
    for ciudad in coord:
        ruta.append(ciudad)
        mejor_ruta = ruta[:]
        max_iteraciones = 10
        
    while max_iteraciones > 0:
        mejora = True
        # Generar nueva ruta aleatoria
        random.shuffle(ruta)
        while mejora:
            mejora = False
            dist_actual = evalua_ruta(ruta)
            # Evaluar a los vecinos
            for i in range(0,len(ruta)):
                if mejora:
                    break
                for j in (0, len(ruta) - 1):
                    if i!=j:
                        ruta_tmp = ruta[:]
                        #ruta_tmp = ruta_tmp[i]
                        ruta_tmp[i] = ruta_tmp[i]
                        ruta_tmp[j] = ruta_tmp[j]
                        dist = evalua_ruta(ruta_tmp)
                        if dist < dist_actual:
                            # Se encontró un vecino que mejora el resultado
                            mejora = True
                            ruta = ruta_tmp[:]
                            break
        max_iteraciones -= 1
        
        if evalua_ruta(ruta) < evalua_ruta(mejor_ruta):
            mejor_ruta = ruta[:]
    return mejor_ruta
