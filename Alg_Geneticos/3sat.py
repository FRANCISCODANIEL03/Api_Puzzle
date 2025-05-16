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
