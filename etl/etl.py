import pandas as pd
import mysql.connector
import json
import os

def calcular_estado_academico(promedio):
    if pd.isna(promedio):
        return "Riesgo Académico"
    if promedio >= 16.0:
        return "Destacado"
    elif promedio >= 10.5:
        return "Regular"
    else:
        return "Riesgo Académico"

def calcular_condicion_beca(promedio, creditos):
    if pd.isna(promedio) or pd.isna(creditos):
        return "Sin Beneficio"
    if promedio >= 17.0 and creditos >= 18:
        return "Beca Completa"
    elif promedio >= 15.5:
        return "Media Beca"
    else:
        return "Sin Beneficio"

def ejecutar_etl():
    # Rutas relativas seguras
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '../data/alumnos_universidad_sucio_v2.csv')
    config_path = os.path.join(base_dir, 'config.json')

    print("1. Leyendo archivo CSV crudo...")
    df = pd.read_csv(csv_path)
    print(f"Registros iniciales leídos: {len(df)}")

    # Limpieza de datos: eliminar duplicados y descartar nulos en campos obligatorios
    df = df.drop_duplicates()
    df = df.dropna(subset=['id_alumno', 'nombre_completo', 'facultad', 'carrera'])
    
    # Estandarización de textos
    df['nombre_completo'] = df['nombre_completo'].str.strip().str.title()
    df['facultad'] = df['facultad'].str.strip().str.title()
    df['carrera'] = df['carrera'].str.strip().str.title()

    # Limpieza de valores numéricos
    df['promedio_ponderado'] = pd.to_numeric(df['promedio_ponderado'], errors='coerce').fillna(0)
    df['creditos_matriculados'] = pd.to_numeric(df['creditos_matriculados'], errors='coerce').fillna(0)
    df['semestre'] = pd.to_numeric(df['semestre'], errors='coerce').fillna(1).astype(int)

    # Filtrar rangos lógicos de notas
    df = df[(df['promedio_ponderado'] >= 0) & (df['promedio_ponderado'] <= 20)]

    # Creación de columnas calculadas obligatorias
    df['estado_academico'] = df['promedio_ponderado'].apply(calcular_estado_academico)
    df['condicion_beca'] = df.apply(lambda row: calcular_condicion_beca(row['promedio_ponderado'], row['creditos_matriculados']), axis=1)

    print(f"Registros limpios listos para cargar: {len(df)}")

    # Carga a MySQL
    with open(config_path, 'r') as f:
        config = json.load(f)

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Limpiar tabla antes de insertar (para evitar duplicados en re-ejecuciones)
    cursor.execute("DELETE FROM alumnos;")

    query = """
        INSERT INTO alumnos (id_alumno, nombre_completo, facultad, carrera, semestre, promedio_ponderado, creditos_matriculados, estado_academico, condicion_beca)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        cursor.execute(query, (
            str(row['id_alumno']),
            str(row['nombre_completo']),
            str(row['facultad']),
            str(row['carrera']),
            int(row['semestre']),
            float(row['promedio_ponderado']),
            int(row['creditos_matriculados']),
            str(row['estado_academico']),
            str(row['condicion_beca'])
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("¡ETL ejecutado con éxito y datos cargados en MySQL!")

if __name__ == "__main__":
    ejecutar_etl()