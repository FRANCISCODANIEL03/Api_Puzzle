import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def distancia(coord1, coord2):
    lat1, long1 = coord1
    lat2, long2 = coord2
    return math.sqrt((lat1 - lat2) ** 2 + (long1 - long2) ** 2)

def evalua_ruta(ruta, coord):
    return sum(distancia(coord[ruta[i]], coord[ruta[i+1]]) for i in range(len(ruta)-1))

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

def conectar_base_datos(nombre_imagen, id_imagen):
    conexion = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    cursor = conexion.cursor()
    with open(nombre_imagen, "rb") as file:
        imagen_binaria = file.read()
    sql = """
    INSERT INTO imagenes (id, imagen) VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE imagen = VALUES(imagen)
    """
    cursor.execute(sql, (id_imagen, imagen_binaria))
    conexion.commit()
    cursor.close()
    conexion.close()


def graficar_ruta_nx(ruta, coord, titulo, nombre_archivo, id_imagen):
    G = nx.DiGraph()
    leyenda = {}

    for i, ciudad in enumerate(ruta):
        numero = i + 1
        G.add_node(numero, pos=coord[ciudad])
        leyenda[numero] = ciudad

    for i in range(len(ruta) - 1):  # No cerrar el ciclo
        G.add_edge(i + 1, i + 2)

    pos = nx.spring_layout(G, seed=42)  # diseño automático
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', edge_color='gray', font_weight='bold')

    leyenda_texto = "\n".join(f"{num}. {nombre}" for num, nombre in leyenda.items())
    plt.title(titulo)
    plt.figtext(0.98, 0.5, leyenda_texto, va="center", ha="left", fontsize=9,
                bbox=dict(facecolor='white', edgecolor='gray'))
    plt.tight_layout()
    plt.savefig(nombre_archivo)
    plt.close()

    # Guardar en la base de datos
    conectar_base_datos(nombre_archivo, id_imagen)



if __name__ == "__main__":
    coord = {
        'Jiloyork': (19.916012, -99.580580),
        'Toluca': (19.289165, -99.655697),
        'Atlacomulco': (19.799520, -99.873844),
        'Guadalajara': (20.677754, -103.346254),
        'Monterrey': (25.691611, -100.321838),
        'QuintanaRoo': (21.163112, -86.802315),
        'Michohacan': (19.701400, -101.208297),
        'Aguascalientes': (21.876410, -102.264387),
        'CDMX': (19.432713, -99.133183),
        'QRO': (20.597194, -100.386670)
    }

    ruta = list(coord.keys())
    random.shuffle(ruta)


    
    graficar_ruta_nx(ruta, coord, "Ruta Inicial", "ruta_inicial.png", id_imagen=1)
    mejor_ruta = busqueda_tabu(ruta, coord)
    graficar_ruta_nx(mejor_ruta, coord, "Mejor Ruta con Búsqueda Tabú", "ruta_optima.png", id_imagen=2)
    
    print("Distancia inicial: ", evalua_ruta(ruta, coord))
    print("Distancia optimizada: ", evalua_ruta(mejor_ruta, coord))
