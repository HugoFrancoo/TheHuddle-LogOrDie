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

def init_db():
    conn, cursor = conectar_db()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs(
            id_log SERIAL PRIMARY KEY,
            occurred_at TIMESTAMP NOT NULL,
            received_at TIMESTAMP NOT NULL,
            service VARCHAR(100) NOT NULL,
            severity VARCHAR(100) NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

#funcion encargada de insertar los logs en la base de datos
def insertar_logs(logs_list):
    conn, cursor = conectar_db()
    #se realiza el insert de los logs con los campos correpondientes %s hace referencia a un placeholder marcador de posicion
    insert_logs= ('INSERT INTO logs (occurred_at,received_at,service,severity,message) VALUES (%s, %s, %s, %s, %s)')
    datos = [(log["occurred_at"], datetime.utcnow(), log["service"], log["severity"], log["message"]) for log in logs_list]
    cursor.executemany(insert_logs, datos)
    conn.commit()

def consultar_logs(occurred_at_start=None, occurred_at_end=None,received_at_start=None, received_at_end=None):
    # query base, el WHERE 1=1 permite agregar filtros opcionales con AND sin romper la sintaxis
    query = "SELECT * FROM logs WHERE 1=1"
    params = []
    if occurred_at_start:
        query += " AND occurred_at >= %s"
        params.append(occurred_at_start)
    if occurred_at_end:
        query += " AND occurred_at <= %s"
        params.append(occurred_at_end)
    if received_at_start:
        query += " AND received_at >= %s"
        params.append(received_at_start)
    if received_at_end:
        query += " AND received_at <= %s"
        params.append(received_at_end)

    #conecta a la base de datos
    conn, cursor = conectar_db()
    #ordenar las fechas de received_at en orden DESC 
    query += " ORDER BY received_at DESC"
    #ejecuta la query construida pasando los valores de los filtros como parámetros seguros
    cursor.execute(query, params)
    #almacena en la variable resultado una lista con el resultado de las consultas
    resultados = cursor.fetchall()
    #cierra las conexiones
    cursor.close()
    conn.close()
    return resultados