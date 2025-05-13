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

def en_ruta(rutas, ciudad):
    for r in rutas:
        if ciudad in r:
            return r
    return None

# --------------------------- Algoritmo VRP ------------------------------

def vrp_voraz(coord, pedidos, almacen, max_carga, max_clientes, restricciones_trafico):
    # Calcular los ahorros 
    s = {}
    for c1 in coord:
        for c2 in coord:
            if c1 != c2 and not (c2, c1) in s:
                if not esta_restringido(c1, c2, restricciones_trafico):
                    d_c1_c2 = distancia(coord[c1], coord[c2])
                    d_c1_almacen = distancia(coord[c1], almacen)
                    d_c2_almacen = distancia(coord[c2], almacen)
                    s[c1, c2] = d_c1_almacen + d_c2_almacen - d_c1_c2

    s = sorted(s.items(), key=itemgetter(1), reverse=True)

    rutas = []
    for k, v in s:
        rC1 = en_ruta(rutas, k[0])
        rC2 = en_ruta(rutas, k[1])

        if rC1 == None and rC2 == None:
            nueva_ruta = [k[0], k[1]]
            if (peso_ruta(nueva_ruta, pedidos) <= max_carga and
                clientes_en_ruta(nueva_ruta) <= max_clientes):
                rutas.append(nueva_ruta)

        elif rC1 != None and rC2 == None:
            if rC1[0] == k[0]:
                if (peso_ruta(rC1, pedidos) + pedidos[k[1]] <= max_carga and
                    clientes_en_ruta(rC1) + 1 <= max_clientes):
                    rutas[rutas.index(rC1)].insert(0, k[1])
            elif rC1[-1] == k[0]:
                if (peso_ruta(rC1, pedidos) + pedidos[k[1]] <= max_carga and
                    clientes_en_ruta(rC1) + 1 <= max_clientes):
                    rutas[rutas.index(rC1)].append(k[1])

        elif rC1 == None and rC2 != None:
            if rC2[0] == k[1]:
                if (peso_ruta(rC2, pedidos) + pedidos[k[0]] <= max_carga and
                    clientes_en_ruta(rC2) + 1 <= max_clientes):
                    rutas[rutas.index(rC2)].insert(0, k[0])
            elif rC2[-1] == k[1]:
                if (peso_ruta(rC2, pedidos) + pedidos[k[0]] <= max_carga and
                    clientes_en_ruta(rC2) + 1 <= max_clientes):
                    rutas[rutas.index(rC2)].append(k[0])

        elif rC1 != None and rC2 != None and rC1 != rC2:
            total_peso = peso_ruta(rC1, pedidos) + peso_ruta(rC2, pedidos)
            total_clientes = clientes_en_ruta(rC1) + clientes_en_ruta(rC2)
            if rC1[0] == k[0] and rC2[-1] == k[1]:
                if total_peso <= max_carga and total_clientes <= max_clientes:
                    rutas[rutas.index(rC2)].extend(rC1)
                    rutas.remove(rC1)
            elif rC1[-1] == k[0] and rC2[0] == k[1]:
                if total_peso <= max_carga and total_clientes <= max_clientes:
                    rutas[rutas.index(rC1)].extend(rC2)
                    rutas.remove(rC2)

    return rutas
# ------------------ Vecindario: Intercambio entre rutas ------------------

def generar_vecinos(solucion, pedidos, max_carga, max_clientes, restricciones):
    vecinos = []
    for i in range(len(solucion)):
        for j in range(len(solucion)):
            if i != j:
                for ci in range(len(solucion[i])):
                    for cj in range(len(solucion[j])):
                        nueva = deepcopy(solucion)
                        nueva[i][ci], nueva[j][cj] = nueva[j][cj], nueva[i][ci]
                        if es_factible(nueva, pedidos, max_carga, max_clientes, restricciones):
                            vecinos.append(nueva)
    return vecinos
