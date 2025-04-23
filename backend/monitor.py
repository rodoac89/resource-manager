import psutil
import time
from tinydb import TinyDB, Query
from datetime import datetime
import threading

def get_system_stats():
    """Captura estadísticas del sistema: CPU, RAM, disco."""
    print("Capturando datos...")
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    disk = psutil.disk_usage('/')
    disk_free = disk.free / (1024 ** 3)  # Convertir a GB
    print("Datos capturados...")
    return {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_free': round(disk_free, 2),
        'timestamp': datetime.now().isoformat()
    }

def monitor_system():
    """Captura y almacena datos cada 5 segundos."""
    db = TinyDB('datos.json')
    estados = db.table('estados')
    
    while True:
        stats = get_system_stats()
        estados.insert(stats)
        print(f"Datos almacenados: {stats}")
        time.sleep(5)

def start_monitoring():
    """Inicia el monitoreo en un hilo separado."""
    print("Iniciando monitoreo del sistema...")
    thread = threading.Thread(target=monitor_system, daemon=True)
    thread.start()

if __name__ == "__main__":
    start_monitoring()
    # Mantener el script corriendo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Monitoreo detenido.")