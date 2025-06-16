from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import deque

app = Flask(__name__)
CORS(app)

# Distancia Manhattan
def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return abs(lat1 - lat2) + abs(lon1 - lon2)

# Evaluación de la ruta total
def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    return total

# Genera vecinos por intercambio de ciudades (sin tocar origen ni destino)
def generar_vecinos(ruta):
    vecinos = []
    for i in range(1, len(ruta) - 1):
        for j in range(i + 1, len(ruta) - 1):
            vecino = ruta[:]
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append((vecino, (ruta[i], ruta[j])))
    return vecinos

# Búsqueda Tabú
def busqueda_tabu(ruta_inicial, coord, max_iter=100, tabu_tam=10):
    mejor_ruta = ruta_inicial[:]
    mejor_costo = evalua_ruta(mejor_ruta, coord)
    ruta_actual = mejor_ruta[:]
    tabu = deque(maxlen=tabu_tam)

    for _ in range(max_iter):
        vecinos = generar_vecinos(ruta_actual)
        mejor_vecino = None
        mejor_vecino_costo = float('inf')
        mejor_movimiento = None

        for vecino, movimiento in vecinos:
            if movimiento in tabu or (movimiento[1], movimiento[0]) in tabu:
                continue

            costo = evalua_ruta(vecino, coord)
            if costo < mejor_vecino_costo:
                mejor_vecino = vecino
                mejor_vecino_costo = costo
                mejor_movimiento = movimiento

        if mejor_vecino is None:
            break

        ruta_actual = mejor_vecino[:]
        tabu.append(mejor_movimiento)

        if mejor_vecino_costo < mejor_costo:
            mejor_ruta = mejor_vecino[:]
            mejor_costo = mejor_vecino_costo

    return mejor_ruta

@app.route('/ruta', methods=['POST'])
def ruta():
    datos = request.get_json()
    coords = datos['coordenadas']
    ciudades_seleccionadas = datos['ruta']  # Ya contiene origen, intermedias y destino en orden

    # Validar existencia de coordenadas
    if not all(ciudad in coords for ciudad in ciudades_seleccionadas):
        return jsonify({"error": "Una o más ciudades no tienen coordenadas"}), 400

    ruta_optima = busqueda_tabu(ciudades_seleccionadas, coords)

    return jsonify({"ruta": ruta_optima, "coordenadas": coords})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
