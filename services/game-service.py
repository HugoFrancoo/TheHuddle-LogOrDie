#libreria para realizar peticiones HTTP al servidor
import requests
#libreria para seleccionar logs y numeros de forma aleatoria
import random 
#libreria para obtener la fecha y hora actual del sistema
from datetime import datetime
#lista de logs falsos con severidad y mensaje para simular eventos del servicio de juego
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

#funcion encargada de solicitar el token al servidor
def pedir_token():
    try:
        #realiza una peticion POST al servidor para obtener el token del servicio
        response = requests.post(
            "http://localhost:5000/auth/token",
            json={"service_name": "game-service"}
        )
        #convierte la respuesta a un diccionario y extrae el token
        data = response.json()
        token = data["token"]
        return token 
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar al servidor, verifica que este corriendo")
        return None
    
#funcion encargada de generar logs falsos aleatorios
def generar_log():
    #selecciona aleatoriamente una severidad y un mensaje de la lista de logs falsos
    severity, message = random.choice(LOGS_FALSOS)
    #genera un numero de sala o jugador aleatorio entre 1000 y 9999
    n = random.randint(1000, 9999)
    #construye el diccionario del log con los campos requeridos
    dict_log = {
        "occurred_at": datetime.now().isoformat(),
        "service": "game-service",
        "severity": severity,
        "message": message.format(n=n)
    }
    return dict_log

#funcion encargada de enviar el log al servidor con el token de autenticacion
def enviar_log(token,log):
    try:
        #realiza una peticion POST al servidor enviando el log y el token en el header
        response = requests.post(
        "http://localhost:5000/logs",
        json=log,
        headers={"Authorization": token}
        )
        return response
    except requests.exceptions.ConnectionError:
        print("No se pudo enviar el log, el servidor no esta disponible")
        return None
    
#punto de entrada del servicio
if __name__ == "__main__":
    #solicita el token al servidor antes de enviar los logs
    token = pedir_token()
    #genera y envia 100 logs falsos al servidor
    for i in range(100):
        log = generar_log()
        response = enviar_log(token, log)
        if response:
            print(response.status_code, response.json())