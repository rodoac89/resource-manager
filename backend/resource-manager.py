from flask import Flask, jsonify, request
from tinydb import TinyDB, Query
from monitor import start_monitoring

app = Flask(__name__)

@app.route('/api/estados', methods=['GET'])
def get_estados():
    """Obtiene todos los estados o filtra por rango de tiempo."""
    db = TinyDB('datos.json')
    estados = db.table('estados')
    
    # Parámetros de consulta opcionales: start_time, end_time (ISO format)
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    if start_time and end_time:
        Estado = Query()
        resultados = estados.search(
            (Estado.timestamp >= start_time) & (Estado.timestamp <= end_time)
        )
    else:
        resultados = estados.all()
    
    return jsonify(resultados)

if __name__ == "__main__":
    # Iniciar el monitoreo en un hilo separado
    start_monitoring()
    # Iniciar el servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=True)