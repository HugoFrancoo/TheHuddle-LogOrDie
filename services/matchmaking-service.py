import requests
import random 
from datetime import datetime
LOGS_FALSOS = [
    ("INFO",    "Jugador #{n} agregado a la cola de búsqueda"),
    ("INFO",    "Partida encontrada para grupo #{n}"),
    ("INFO",    "Emparejamiento completado. Sala #{n} creada"),
    ("WARNING", "Tiempo de búsqueda alto para jugador #{n}"),
    ("WARNING", "Jugador #{n} abandonó la cola de búsqueda"),
    ("ERROR",   "Timeout de búsqueda para jugador #{n}"),
    ("ERROR",   "Fallo al crear sala para grupo #{n}"),
    ("DEBUG",   "Calculando MMR para jugador #{n}"),
    ("DEBUG",   "Buscando partida con rango similar. Jugador #{n}"),
]

def pedir_token():
    response = requests.post(
        "http://localhost:5000/auth/token",
        json={"service_name": "matchmaking-service"}
    )

    data = response.json()
    token = data["token"]
    return token 

def generar_log():
    severity, message = random.choice(LOGS_FALSOS)
    n = random.randint(1000, 9999)

    dict_log = {
        "occurred_at": datetime.now().isoformat(),
        "service": "matchmaking-service",
        "severity": severity,
        "message": message.format(n=n)
    }
    return dict_log

def enviar_log(token,log):
    response = requests.post(
    "http://localhost:5000/logs",
    json=log,
    headers={"Authorization": token}
    )
    return response

if __name__ == "__main__":
    token = pedir_token()
    for i in range(100):
        log = generar_log()
        response = enviar_log(token, log)
        print(response.status_code, response.json())