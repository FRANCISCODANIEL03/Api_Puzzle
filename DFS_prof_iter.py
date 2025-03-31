# Vuelos con busqueda con profundidad iterativa
from Arbol import Nodo

def DFS_prof_iter(nodo, solucion, conexiones):
    for limite in range(0, 100):
        visitados = []
        sol = buscar_solucion_DFS_rec(nodo, solucion, visitados, limite, conexiones)
        if sol is not None:
            return sol
        
def buscar_solucion_DFS_rec(nodo, solucion, visitados, limite, conexiones):
    if limite > 0:
        visitados.append(nodo)
        if nodo.get_datos() == solucion:
            return nodo
        # Expandir los nodos hijo (ciudades con conexion)
        dato_nodo = nodo.get_datos()
        lista_hijos = []
        for un_hijo in conexiones[dato_nodo]:
            if not un_hijo in visitados:
                hijo_nodo = Nodo(un_hijo)
                lista_hijos.append(hijo_nodo)
        nodo.set_hijos(lista_hijos)
        for nodo_hijo in nodo.get_hijos():
            if not nodo_hijo.get_datos() in visitados:
                # Llamada recursiva
                sol = buscar_solucion_DFS_rec(nodo_hijo, solucion, visitados, limite -1, conexiones)
                if sol != None:
                    return sol
        return None