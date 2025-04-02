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

def peso_ruta(ruta, pedidos):
    return sum(pedidos[c] for c in ruta)

def clientes_en_ruta(ruta):
    return len(ruta)

def esta_restringido(ciudad1, ciudad2, restricciones):
    return (ciudad1, ciudad2) in restricciones or (ciudad2, ciudad1) in restricciones

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
