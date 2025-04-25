from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import math
from operator import itemgetter

app = Flask(__name__)
CORS(app)

# Coordenadas fijas
coord = {
    'EDO.MEX': (19.293704, -99.653710),
    'QRO': (20.593507, -100.390073),
    'CDMX': (19.432915, -99.133364),
    'SPL': (22.150933, -100.974140),
    'MTY': (25.675059, -100.287583),
    'PUE': (19.063634, -98.306991),
    'GDL': (20.677205, -103.346995),
    'MICH': (19.702595, -101.192383),
    'SON': (29.075226, -110.959625)
}

# Pedidos fijos
pedidos = {
    'EDO.MEX': 10,
    'QRO': 13,
    'CDMX': 7,
    'SPL': 11,
    'MTY': 15,
    'PUE': 8,
    'GDL': 6,
    'MICH': 7,
    'SON': 8
}

def distancia(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def en_ruta(rutas, ciudad):
    for r in rutas:
        if ciudad in r:
            return r
    return None

def peso_ruta(ruta, pedidos):
    return sum(pedidos[c] for c in ruta)

def clientes_en_ruta(ruta):
    return len(ruta)

def esta_restringido(ciudad1, ciudad2, restricciones):
    return (ciudad1, ciudad2) in restricciones or (ciudad2, ciudad1) in restricciones

def vrp_voraz(almacen, max_carga, max_clientes, restricciones_trafico):
    s = {}
    for c1 in coord:
        for c2 in coord:
            if c1 != c2 and not (c2, c1) in s:
                if not esta_restringido(c1, c2, restricciones_trafico):
                    d_c1_c2 = distancia(coord[c1], coord[c2])
                    d_c1_almacen = distancia(coord[c1], almacen)
                    d_c2_almacen = distancia(coord[c2], almacen)
                    s[c1, c2] = d_c1_almacen + d_c2_almacen - d_c1_c2

    s = sorted(s.items(), key=itemgetter(1), reverse=True)
    rutas = []

    for (c1, c2), _ in s:
        r1 = en_ruta(rutas, c1)
        r2 = en_ruta(rutas, c2)

        if r1 is None and r2 is None:
            nueva_ruta = [c1, c2]
            if peso_ruta(nueva_ruta, pedidos) <= max_carga and clientes_en_ruta(nueva_ruta) <= max_clientes:
                rutas.append(nueva_ruta)

        elif r1 is not None and r2 is None:
            if r1[0] == c1 and peso_ruta(r1, pedidos) + pedidos[c2] <= max_carga and len(r1) + 1 <= max_clientes:
                r1.insert(0, c2)
            elif r1[-1] == c1 and peso_ruta(r1, pedidos) + pedidos[c2] <= max_carga and len(r1) + 1 <= max_clientes:
                r1.append(c2)

        elif r1 is None and r2 is not None:
            if r2[0] == c2 and peso_ruta(r2, pedidos) + pedidos[c1] <= max_carga and len(r2) + 1 <= max_clientes:
                r2.insert(0, c1)
            elif r2[-1] == c2 and peso_ruta(r2, pedidos) + pedidos[c1] <= max_carga and len(r2) + 1 <= max_clientes:
                r2.append(c1)

        elif r1 != r2:
            total_peso = peso_ruta(r1, pedidos) + peso_ruta(r2, pedidos)
            total_clientes = len(r1) + len(r2)
            if r1[0] == c1 and r2[-1] == c2 and total_peso <= max_carga and total_clientes <= max_clientes:
                r2.extend(r1)
                rutas.remove(r1)
            elif r1[-1] == c1 and r2[0] == c2 and total_peso <= max_carga and total_clientes <= max_clientes:
                r1.extend(r2)
                rutas.remove(r2)

    return rutas

@app.route('/vrp', methods=['POST'])
@cross_origin()
def calcular_rutas():
    data = request.get_json()

    almacen = tuple(data['almacen'])
    max_carga = data['max_carga']
    max_clientes = data['max_clientes']
    restricciones_trafico = [tuple(r) for r in data.get('restricciones_trafico', [])]

    rutas = vrp_voraz(almacen, max_carga, max_clientes, restricciones_trafico)

    rutas_detalle = [{
        "ruta": ruta,
        "peso_total": peso_ruta(ruta, pedidos),
        "clientes": len(ruta)
    } for ruta in rutas]

    return jsonify({"rutas": rutas_detalle})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=6000)
