import requests
import random 
from datetime import datetime
LOGS_FALSOS = [
    ("INFO",    "Escaneo de jugador #{n} completado sin anomalías"),
    ("INFO",    "Sistema anticheat iniciado correctamente"),
    ("WARNING", "Comportamiento sospechoso detectado. Jugador #{n}"),
    ("WARNING", "Velocidad de movimiento anormal. Jugador #{n}"),
    ("ERROR",   "Jugador #{n} baneado por uso de hacks"),
    ("ERROR",   "Inyección de memoria detectada. Jugador #{n}"),
    ("DEBUG",   "Analizando paquetes de red. Jugador #{n}"),
    ("DEBUG",   "Verificando integridad de archivos. Jugador #{n}"),
    ("WARNING", "Múltiples reportes recibidos contra jugador #{n}"),
]

def pedir_token():
    response = requests.post(
        "http://localhost:5000/auth/token",
        json={"service_name": "anticheat-service"}
    )

    data = response.json()
    token = data["token"]
    return token 

def generar_log():
    severity, message = random.choice(LOGS_FALSOS)
    n = random.randint(1000, 9999)

    dict_log = {
        "occurred_at": datetime.utcnow().isoformat(),
        "service": "anticheat-service",
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