from Arbol import Nodo
import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector

def conectar_base_datos():
    # Conexión a la base de datos
    conexion = mysql.connector.connect(
        host="bltpsedcjatmi5mobxi6-mysql.services.clever-cloud.com",
        user="uzfprw81c47ssrq8",
        password="IbRqoqg9GZU4ln01Z0V4",
        database="bltpsedcjatmi5mobxi6"
    )

    cursor = conexion.cursor()

    # Leer imagen como binario
    with open("grafo.png", "rb") as file:
        imagen_binaria = file.read()

    # Insertar en la base de datos
    sql = "UPDATE imagenes SET imagen = %s WHERE id = %s"
    #sql = "INSERT INTO imagenes (nombre, imagen) VALUES (%s, %s)"
    cursor.execute(sql, (imagen_binaria, 1))

    conexion.commit()
    cursor.close()
    conexion.close()

def dijkstra(grafo, inicio, fin):
    """
    Funcion para encontrar el camino mas corto en un grafo utilizando el algoritmo de Dijkstra
    y la clase "Nodo".
    :param grafo: Grafo representado como un diccionario.
    :param inicio: Nodo de inicio.
    :param fin: Nodo de destino.
    :return: Distancia mas corta y el camino tomado.
    """
    # Incializar el grafo
    nodos = {nodo: Nodo(nodo) for nodo in grafo}
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos.items():
            nodos[nodo].set_hijos([nodos[vecino]])
            nodos[vecino].set_costo(peso)
    # Inicializar las distancias y nodos previos
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    nodos_previos = {nodo: None for nodo in grafo}
    nodos_no_visitados = list(grafo.keys())
    # Bucle principal
    while nodos_no_visitados:
        # Encontrar el nodo con la distancia mas corta
        nodo_actual = min(nodos_no_visitados, key=lambda nodo: distancias[nodo])
        nodos_no_visitados.remove(nodo_actual)

        # Si llegamos al destino, salir
        if nodo_actual == fin:
            break

        # Actualizar distancias para los vecinos
        for vecino in grafo[nodo_actual]:
            if vecino in nodos_no_visitados:
                nueva_distancia = distancias[nodo_actual] + grafo[nodo_actual][vecino]
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    nodos_previos[vecino] = nodo_actual
    # Reconstruir el camino
    camino = []
    nodo_actual = fin
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual = nodos_previos[nodo_actual]
    camino.reverse()
    # Retornar la distancia mas corta y el camino tomado
    return distancias[fin], camino
    
def representar_graficamente(grafo, camino):
    """
    Funcion para representar el grafo y el camino tomado.
    :param grafo: El grafo representado como un diccionario.
    :param camino: El camino tomado.
    """
    plt.clf()

    G = nx.Graph()

    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos.items():
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, pos, with_labels=True,  node_size=1000, node_color='skyblue', font_size=12)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    # Resaltar el camino
    aristas_camino = [(camino[i], camino[i + 1]) for i in range(len(camino) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=aristas_camino, edge_color='r', width=4)

    # Guardar la figura
    plt.savefig("grafo.png")
    conectar_base_datos()
    plt.close()

"""
if __name__ == "__main__":
    # Pedir al usuario que ingrese el grafo
    nodos = input("Ingresa el numero de nodos del grafo: --> ")
    grafo = {}
    for i in range(int(nodos)):
        nodo = i + 1
        nodo = str(nodo)
        grafo[nodo] = {}
        for j in range(int(nodos)):
            if i != j: 
                # Preguntar al usuario el peso de la arista solo si no se ha ingresado antes
                # ejemplo 1-2 y 2-1 son la misma arista entonces no se vuelve a preguntar 
                if i + 1 in grafo[nodo]:
                    continue
                else:
                    peso = input(f"Ingrese el peso de la arista entre {nodo} y {j + 1}: ")
                # Si el peso es vacio no se agrega la arista
                if peso == "":
                    continue
                # Si el peso es cero no se agrega la arista
                if peso == "0":
                    continue
                # si el peso es negativo no se agrega la arista
                if peso[0] == "-":
                    continue
                peso = int(peso)
                grafo[nodo][str(j + 1)] = int(peso)
    print(grafo)

    grafo = {
        '1':{'2': 3,'3': 6},
        '2':{'1': 3,'3': 2, '4': 1},
        '3':{'1': 6,'2': 2, '4': 4, '5': 2},
        '4':{'2': 1,'3': 4,'5': 6},
        '5':{'3': 2,'4': 6, '6': 2,'7': 2},
        '6':{'5': 2,'7': 3},
        '7':{'5': 2,'6': 3}
    }

    # verificar si el grafo es valido
    nodo_inicio = input("Ingresa el nodo de inicio: --> ")
    nodo_fin = input("Ingresa el nodo de fin: --> ")

    distancia, camino = dijkstra(grafo, nodo_inicio, nodo_fin)
    # Imprimir la distancia y el camino
    print(f"Shortest distance: {distancia}")
    print(f"Path taken: {camino}")
    representar_graficamente(grafo, camino)
"""

