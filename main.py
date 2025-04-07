from flask import Flask, jsonify,request
from flask_cors import CORS, cross_origin
from dijkstra import dijkstra, representar_graficamente

app = Flask(__name__)
CORS(app)

@app.route("/grafo", methods = ["POST"])
@cross_origin()
def nodos():
    body = request.json
    print(body)
    grafo = body['grafo']
    nodo_inicial = body['nodoInicial']
    nodo_final = body['nodoFinal']
    
    distancia, camino = dijkstra(grafo, nodo_inicial, nodo_final)
    # Imprimir la distancia y el camino
    print(f"Shortest distance: {distancia}")
    print(f"Path taken: {camino}")
    representar_graficamente(grafo, camino)
    return jsonify(distancia, camino)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=6000)

