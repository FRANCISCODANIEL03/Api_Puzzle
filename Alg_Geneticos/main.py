from flask import Flask, jsonify, request
from flask_cors import CORS
import math
import random

def poblacion_inicial(max_poblacion, num_vars):
    # Crear población inicial aleatoria
    poblacion = []
    for i in range(max_poblacion):
        gen=[]
        for j in range(num_vars):
            if random.random() > 0.5:
                gen.append(1)
            else:
                gen.append(0)
        poblacion.append(gen[:])
    return poblacion

def adaptacion_3sat(gen, solucion):
    # Contar Cláusulas correctas
    n = 3
    cont = 0
    clausula_ok = True
    for i in range(len(gen)):
        n = n-1
        if (gen[i] != solucion[i]):
            clausula_ok = False
            if n == 0:
                if clausula_ok:
                    cont = cont + 1
                n = 3
                clausula_ok = True
        if n > 0:
            if clausula_ok:
                cont = cont + 1
            return cont
