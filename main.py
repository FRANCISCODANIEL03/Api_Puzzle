from flask import Flask, jsonify,request
from flask_cors import CORS, cross_origin
from dijkstra import dijkstra, representar_graficamente
import mysql.connector
from dotenv import load_dotenv
import os
from flask import send_file
import io

load_dotenv()

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



@app.route("/imagen", methods=["GET"])
@cross_origin()
def obtener_imagen():
    conexion = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

    cursor = conexion.cursor()
    cursor.execute("SELECT imagen FROM imagenes WHERE id = %s", (1,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if resultado and resultado[0]:
        imagen_binaria = resultado[0]
        return send_file(io.BytesIO(imagen_binaria), mimetype='image/png')
    else:
        return "Imagen no encontrada", 404


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=6000)

