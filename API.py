from flask import Flask, jsonify,request
from flask_cors import CORS, cross_origin
from Arbol import Nodo
from DFS_rec import buscar_solucion_DFS_rec
from BFS import buscar_solucion_BFS
from DFS import buscar_solucion_DFS

app = Flask(__name__)
CORS(app)

@app.route("/dfs-rec", methods = ["POST"])
@cross_origin()
def solucion():
    body = request.json
    print(body)
    i = body['estadoInicial']
    s = body['solucion']
    estado_inicial = i
    solucion = s
    visitados = []
    nodo_inicial = Nodo(estado_inicial)
    nodo = buscar_solucion_DFS_rec(nodo_inicial, solucion, visitados)
    # Mostrar resultado 
    resultado = []
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()

    resultado.append(estado_inicial)
    resultado.reverse()
    return str(resultado)

@app.route("/bfs", methods = ["POST"])
@cross_origin()
def solucion_bfs():
    conexiones = {
        'CDMX': {'SLP','MEXICALI', 'CHIHUAHUA'},
        'SAPOPAN': {'ZACATECAS', 'MEXICALI'},
        'GUADALAJARA':{'CHIAPAS'},
        'VHIAPAS':{'CHIHUAHUA'},
        'MEXICALI':{'SLP', 'SAPOPAN', 'CDMX', 'CHIHUAHUA', 'SONORA'},
        'SLP':{'CDMX', 'MEXICALI'},
        'ZACATECAS':{'SAPOPAN', 'SONORA', 'CHIHUAHUA'},
        'SONORA':{'ZACATECAS', 'MEXICALI'},
        'MICHOACAN':{'CHIHUAHUA'},
        'CHIHUAHUA':{'MICHOACAN', 'ZACATECAS', 'MEXICALI', 'CDMX','CHIAPAS' }
    }
    body = request.json
    estado_inicial = body['estadoInicial']
    solucion = body['destino']
    nodo_solucion = buscar_solucion_BFS(conexiones, estado_inicial, solucion)
    # Mostrar Resultado
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() != None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()
    return str(resultado)

@app.route("/dfs", methods=["POST"])
@cross_origin()
def solucion_dfs():
    body = request.json
    estado_inicial = body['estadoInicial']
    solucion = body['solucion']
    nodo_solucion = buscar_solucion_DFS(estado_inicial, solucion)
    # Mostrar resultado 
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()

    resultado.append(estado_inicial)
    resultado.reverse()
    return str(resultado)
if __name__ == '__main__':
    app.run()

