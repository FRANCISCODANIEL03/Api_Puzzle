from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from HILL_C import hill_climbing, evalua_ruta

app = Flask(__name__)
CORS(app)
