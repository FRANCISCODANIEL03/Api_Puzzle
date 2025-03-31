import time

def obtener_frecuencia_cpu():
    """Obtiene la frecuencia del CPU en Hz."""
    try:
        # En Linux, intenta leer la frecuencia desde /proc/cpuinfo
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "cpu MHz" in line:
                    frecuencia_mhz = float(line.split(":")[1].strip())
                    return frecuencia_mhz * 1e6  # Convertir MHz a Hz
    except:
        pass

    # Si no se puede obtener, devuelve un valor predeterminado (3 GHz)
    return 3e9

def medir_ciclos(codigo, repeticiones=1):
    """Mide los ciclos de reloj que tarda en ejecutarse un código."""
    frecuencia_cpu = obtener_frecuencia_cpu()
    
    if frecuencia_cpu is None:
        raise RuntimeError("No se pudo obtener la frecuencia del CPU")

    inicio = time.perf_counter_ns()  # Tiempo en nanosegundos
    for _ in range(repeticiones):
        codigo()
    fin = time.perf_counter_ns()

    tiempo_segundos = (fin - inicio) / 1e9  # Convertir nanosegundos a segundos
    ciclos = tiempo_segundos * frecuencia_cpu
    return int(ciclos)

# Ejemplo de uso
def mi_codigo():
    suma = 0
    for i in range(1000):
        suma += i

