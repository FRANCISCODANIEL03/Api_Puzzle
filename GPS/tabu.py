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
