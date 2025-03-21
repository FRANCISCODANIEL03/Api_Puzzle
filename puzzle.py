# Puzzle lineal con busqueda en amplitud 
from Arbol import Nodo

def buscar_solucion_BFS(estado_inical, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inical)
    nodos_frontera.append(nodo_inicial)
    while not solucionado and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)
        # Extraer el nodo y añadirlo a visitados 
        nodos_visitados.append(nodo)
        if nodo.get_datos() == solucion:
            # Solucion encontrada
            solucionado = True
            return nodo
        else: 
            # Expandir los nodos hijo
            dato_nodo = nodo.get_datos()

            # Operador izquierdo
            hijo = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
            hijo_izq = Nodo(hijo)
            hijo_izq.padre = nodo
            if not hijo_izq.en_lista(nodos_visitados)\
                and not hijo_izq.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_izq)
                
            # Operador medio
            hijo = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
            hijo_medio = Nodo(hijo)
            hijo_medio.padre = nodo
            if not hijo_medio.en_lista(nodos_visitados)\
                and not hijo_medio.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_medio)

            # Operador derecho
            hijo = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
            hijo_der = Nodo(hijo)
            hijo_der.padre = nodo
            if not hijo_der.en_lista(nodos_visitados)\
                and not hijo_der.en_lista(nodos_frontera):
                nodos_frontera.append(hijo_der)

if __name__ == "__main__":
    estado_inicial = [4,2,3,1]
    solucion = [1,2,3,4]
    nodo_solucion = buscar_solucion_BFS(estado_inicial, solucion)
    # Mostrar resultado 
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()

    resultado.append(estado_inicial)
    resultado.reverse()
    print(resultado)

    # Resultado
    # [[4,2,3,1], [2,4,3,1], [2,3,1,4], [2,1,3,4], [1,2,3,4]]
