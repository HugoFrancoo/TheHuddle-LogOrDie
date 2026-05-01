import psycopg2
from datetime import datetime
#conexion con la db 
def conectar_db():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="12345",
        database="LogOrDIe"
    )
    cursor = conn.cursor()
    return conn ,cursor

def insertar_logs(logs_list):
    conn, cursor = conectar_db()
    #se realiza el insert de los logs con los campos correpondientes %s hace referencia a un placeholder marcador de posicion
    insert_logs= ('INSERT INTO logs (occurred_at,received_at,service,severity,message) VALUES (%s, %s, %s, %s, %s)')
    datos = [(log["occurred_at"], datetime.utcnow(), log["service"], log["severity"], log["message"]) for log in logs_list]
    cursor.executemany(insert_logs, datos)
    conn.commit()

def consultar_logs():
    conn, cursor = conectar_db()
    cursor.execute("SELECT * FROM logs ORDER BY received_at DESC")
    resultados = cursor.fetchall()
    return resultados