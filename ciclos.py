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
