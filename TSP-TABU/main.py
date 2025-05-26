from flask import Flask, jsonify
from flask_cors import CORS
import random
from tabu_db import busqueda_tabu, evalua_ruta

app = Flask(__name__)
CORS(app)

@app.route("/ruta", methods=["GET"])
def procesar_ruta():
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

    mejor_ruta = busqueda_tabu(ruta, coord)

    return jsonify({
        "ruta_inicial": ruta,
        "mejor_ruta": mejor_ruta,
        "distancia_inicial": evalua_ruta(ruta, coord),
        "distancia_optimizada": evalua_ruta(mejor_ruta, coord)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
