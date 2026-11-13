from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import json
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir peticiones desde Angular

def obtener_conexion():
    # Usamos el mismo archivo de configuración del ETL
    config_path = os.path.join(os.path.dirname(__file__), '../etl/config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    return mysql.connector.connect(**config)

@app.route('/api/alumnos', methods=['GET'])
def get_alumnos():
    """Endpoint para listar todos los alumnos limpios (para la tabla de Angular)"""
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumnos")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado)

@app.route('/api/estadisticas/facultad', methods=['GET'])
def get_est_facultad():
    """Endpoint para el Gráfico de Barras: Alumnos por Facultad"""
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT facultad, COUNT(*) as total 
        FROM alumnos 
        GROUP BY facultad
    """
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado)

@app.route('/api/estadisticas/estado', methods=['GET'])
def get_est_estado():
    """Endpoint para el Gráfico de Dona: Estado Académico (Destacado, Regular, Riesgo)"""
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT estado_academico, COUNT(*) as total 
        FROM alumnos 
        GROUP BY estado_academico
    """
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado)

if __name__ == '__main__':
    print("Iniciando microservicio Backend en http://localhost:5000 ...")
    app.run(debug=True, port=5000)