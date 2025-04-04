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

# ---------------------------- Ejecución ----------------------------

if __name__ == "__main__":
    coord = {
        'EDO.MEX': (19.29370432359307, -99.65371080401178),
        'QRO': (20.593507359686654, -100.39007276165671),
        'CDMX': (19.43291511136525, -99.13336444220519),
        'SPL': (22.15093335177082, -100.97414039898334),
        'MTY': (25.67505869471195, -100.28758283172263),
        'PUE': (19.063633672407946, -98.3069909799001),
        'GDL': (20.677204573193357, -103.34699475549439),
        'MICH': (19.702594693971918, -101.1923828770145),
        'SON': (29.075226304565465, -110.95962477492)
    }

    pedidos = {
        'EDO.MEX': 10,
        'QRO': 13,
        'CDMX': 7,
        'SPL': 11,
        'MTY': 15,
        'PUE': 8,
        'GDL': 6,
        'MICH': 7,
        'SON': 8
    }

    almacen = [19.43291511136525, -99.13336444220519] # CDMX
    max_carga = 20
    max_clientes = 5

    restricciones_trafico = [
        ('QRO', 'PUE'),
        ('MTY', 'SPL'),
        ('SON', 'GDL')
    ]
