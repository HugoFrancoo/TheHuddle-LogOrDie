# Enviar un log al servidor
# En este ejercicio, debes completar la función enviar_log que envía un log al servidor central utilizando la biblioteca requests.
# para saber el endpoint de destino verirficar la documentacion de la API https://live-coding-server.onrender.com

import requests

token = 'token_super_secreto_123'

url = 'https://live-coding-server.onrender.com/logging/logs' # verificar en la documentacion

log = {
    "timestamp": "2024-08-27T12:00:00",
    "service_name": "ServicioEjemplo",
    "severity": "WARNING",
    "message": "Alerta de sistema"
}

def enviar_log(log, url, token):
    # headers = {'Accept': 'application/json'}
    headers = {"Authorization": token}

    response = requests.post(url,headers=headers, json=log)

    if response.status_code == 201:
        print("funciona")
        return True
    else:
        print(response.status_code)
        return False
    # 1. Configurar los headers con el token de autorización
    # 2. Enviar una solicitud POST al servidor con el log
    # 3. Verificar si la solicitud fue exitosa (código de estado 201)
    # 4. Retornar True si fue exitoso, False si no
    pass

enviar_log(log,url,token)
# utiliza tu funcion para enviar tu los al servicio de logs