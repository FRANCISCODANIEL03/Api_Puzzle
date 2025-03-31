# Vuelos con busqueda con profundidad iterativa
from Arbol import Nodo

def DFS_prof_iter(nodo, solucion, conexiones):
    for limite in range(0, 100):
        visitados = []
        sol = buscar_solucion_DFS_rec(nodo, solucion, visitados, limite, conexiones)
        if sol is not None:
            return sol
        