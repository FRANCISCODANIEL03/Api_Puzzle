# TSP con templado simulado
import math
import random

def distancia(coord1, coord2):
    lat1 = coord1[0]
    long1 = coord1[1]
    lat2 = coord2[0]
    long2 = coord2[1]

    return math.sqrt((lat1 - lat2) ** 2 + (long1 - long2) ** 2)

# Calcular al distancia cunierta por una ruta
def evalua_ruta(ruta, coord):
    total = 0
    for i in range(0, len(ruta)-1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i+1]
        total = total + distancia(coord[ciudad1], coord[ciudad2])

    ciudad1 = ruta[i+1]
    ciudad2 = ruta[0]
    total = total + distancia(coord[ciudad1], coord[ciudad2])

    return total

def simulated_annealing(ruta, coord, temp):
    T = temp
    T_min = 0
    v_enfriamiento = 100
    
    while T > T_min:
        dist_actual = evalua_ruta(ruta, coord)
        for i in range(1, v_enfriamiento):
            #Intercambio de dos ciudades aleatoriamente
            i = random.randint(0, len(ruta)-1)
            j = random.randint(0, len(ruta)-1)
            ruta_tmp = ruta[:]

            ciudad_tmp = ruta_tmp[i]
            ruta_tmp[i] = ruta_tmp[j]
            ruta_tmp[j] = ciudad_tmp

            dist_evalua_ruta = evalua_ruta(ruta_tmp, coord)

            delta = dist_actual - dist_evalua_ruta

            if(delta < dist_evalua_ruta):
                ruta = ruta_tmp[:]
                break

        #Enfriar a T linealmente
        T = T - 0.005

    
    return ruta

if __name__ == "__main__":
    coord = {
        'Jiloyork' :(19.916012, -99.580580),
        'Toluca':(19.289165, -99.655697),
        'Atlacomulco':(19.799520, -99.873844),
        'Guadalajara':(20.677754472859146, -103.34625354877137),
        'Monterrey':(25.69161110159454, -100.321838480256),
        'QuintanaRoo':(21.163111924844458, -86.80231502121464),
        'Michohacan':(19.701400113725654, -101.20829680213464),
        'Aguascalientes':(21.87641043660486, -102.26438663286967),
        'CDMX':(19.432713075976878, -99.13318344772986),
        'QRO':(20.59719437542255, -100.38667040246602)
    }

    #Crear una ruta inicial aleatoria
    ruta = []
    temp = 20
    for ciudad in coord:
        ruta.append(ciudad)

    random.shuffle(ruta)

    print(ruta)
    mejor_ruta = simulated_annealing(ruta, coord, temp)
    print(mejor_ruta)
    print("Distnacia total mejorada" + str(evalua_ruta(mejor_ruta, coord)))
    print("Distancia total: " + str(evalua_ruta(ruta, coord)))
