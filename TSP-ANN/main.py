from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from TSP import evalua_ruta, simulated_annealing
import random

app = Flask(__name__)
CORS(app)

@app.route('/tsp_mj', methods=['POST'])
@cross_origin()
def calcular_rutas():
    temp = request.json.get('temp')

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

    for ciudad in coord:
        ruta.append(ciudad)

    random.shuffle(ruta)

    #print(ruta)
    mejor_ruta = simulated_annealing(ruta, coord, temp)
    #print(mejor_ruta)
    Distancia_total_mejorada =  str(evalua_ruta(mejor_ruta, coord))
    Distancia_total = str(evalua_ruta(ruta, coord))

    datos = {
        "ruta": ruta,
        "distancia_total": Distancia_total,
        "ruta_mejorada": mejor_ruta,
        "distancia_total_mj": Distancia_total_mejorada,
    }

    return jsonify(datos)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001)
