from flask import Flask,jsonify,request
from datetime import datetime
from flask_cors import CORS
from mongoengine import connect
from bson import ObjectId
from models import Miembro,Evento,Asistencia,Donacion,TipoDonacion
app = Flask(__name__)
CORS(app)  # Aplica CORS a tu aplicación Flask
# Conexión a MongoDB con MongoEngine usando la cadena de conexión SRV
connect('dbiglesia', host='mongodb+srv://username:password@clusteriglesia.4epxwxo.mongodb.net?retryWrites=true&w=majority&appName=ClusterIglesia')

@app.route('/')
def hello():
    return 'Bienvenido a mi API con Flask y GraphQL!'
@app.route('/eventos', methods=['GET'])
def get_eventos():
    eventos = Evento.objects().to_json()
    return eventos, 200

@app.route('/miembros', methods=['GET'])
def get_miembros():
    miembros = Miembro.objects().to_json()
    return miembros, 200

@app.route('/asistencias', methods=['GET'])
def get_asistencias():
    asistencias = Asistencia.objects().to_json()
    return asistencias, 200

@app.route('/eventos_con_asistencia_fecha', methods=['POST'])
def get_eventos_con_asistencia_fecha():
    # Obtener las fechas como cadenas del formato 'YYYY-MM-DD' desde el cuerpo de la solicitud JSON
    data = request.json
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    
    # Convertir las cadenas de fecha a objetos datetime
    start_date = datetime.fromisoformat(start_date_str)
    end_date = datetime.fromisoformat(end_date_str)

    # Filtrar eventos por fecha
    eventos_filtrados = []
    eventoAll = Evento.objects()
    print(len(eventoAll))
    for evento in eventoAll:
        fechaFormat = datetime.fromisoformat(evento.fecha)
        if start_date <= fechaFormat <= end_date:
            eventos_filtrados.append(evento)

    # Calcular la cantidad de asistencias por evento y construir la lista de eventos con asistencias
    eventos_con_asistencia = []

    for evento in eventos_filtrados:
        cantidad_asistencias = Asistencia.objects(eventoId=str(evento.id)).count()
        evento_dict = {
            'id': str(evento.id),
            'nombre': evento.nombre,
            'fecha': evento.fecha,
            'lugar': evento.lugar,
            'cantidad_asistencias': cantidad_asistencias
        }
        eventos_con_asistencia.append(evento_dict)

    # Ordenar eventos por cantidad de asistencias de mayor a menor
    eventos_con_asistencia_sorted = sorted(eventos_con_asistencia, key=lambda x: x['cantidad_asistencias'], reverse=True)

    return jsonify(eventos_con_asistencia_sorted), 200

@app.route('/recaudacion_eventos', methods=['GET'])
def recaudacion_eventos():
    try:
        recaudaciones = Evento.obtener_recaudacion_eventos()
        recaudaciones_dict = []
        for recaudacion in recaudaciones:
            evento = Evento.objects.get(id=recaudacion['_id'])
            recaudaciones_dict.append({
                'eventoId': str(recaudacion['_id']),
                'nombre_evento': evento.nombre,
                'total_recaudado': recaudacion['total_recaudado']
            })
        
        return jsonify(recaudaciones_dict), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/eventos_con_asistencia', methods=['GET'])
def get_eventos_con_asistencia():
    eventos = Evento.objects()
    eventos_con_asistencia = []

    for evento in eventos:
        cantidad_asistencias = Asistencia.objects(eventoId=str(evento.id)).count()
        evento_dict = {
            'id': str(evento.id),
            'nombre': evento.nombre,
            'fecha': evento.fecha,
            'lugar': evento.lugar,
            'cantidad_asistencias': cantidad_asistencias
        }
        eventos_con_asistencia.append(evento_dict)

    return jsonify(eventos_con_asistencia), 200




if __name__ == '__main__':
    app.run(debug=True)
