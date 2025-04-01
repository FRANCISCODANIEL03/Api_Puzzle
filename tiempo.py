import time

inicio = time.perf_counter()

# Código a medir
suma = 0
for i in range(1, 1000000):
    suma += i


fin = time.perf_counter()
tiempo_total = fin - inicio

print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")
