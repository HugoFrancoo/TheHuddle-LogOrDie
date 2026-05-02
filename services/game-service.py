import requests
import random 
from datetime import datetime
LOGS_FALSOS = [
    ("INFO",    "Partida iniciada. Sala ID: {n}"),
    ("INFO",    "Jugador #{n} se unió a la partida"),
    ("INFO",    "Partida finalizada. Ganador: Jugador #{n}"),
    ("WARNING", "Conexión inestable detectada. Jugador #{n}"),
    ("WARNING", "Tiempo de respuesta alto en sala #{n}"),
    ("ERROR",   "Jugador #{n} desconectado abruptamente"),
    ("ERROR",   "Fallo al guardar resultado de partida #{n}"),
    ("DEBUG",   "Sincronizando estado de sala #{n}"),
    ("DEBUG",   "Tick del servidor procesado. Sala #{n}"),
]

def pedir_token():
    response = requests.post(
        "http://localhost:5000/auth/token",
        json={"service_name": "game-service"}
    )

    data = response.json()
    token = data["token"]
    return token 

def generar_log():
    severity, message = random.choice(LOGS_FALSOS)
    n = random.randint(1000, 9999)

    dict_log = {
        "occurred_at": datetime.utcnow().isoformat(),
        "service": "game-service",
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
    for i in range(10):
        log = generar_log()
        response = enviar_log(token, log)
        print(response.status_code, response.json())