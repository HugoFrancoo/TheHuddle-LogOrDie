#importamos la clase Flask de flask para poder instanciar objetos apartir de el
from flask import Flask, request, jsonify
#importamos las funciones para generar token y para verificarlas
from auth import generar_token, verificar_token
#importamos la funcion insertar_logs para almacenar la informacion en nuestra base de datos
from database import insertar_logs, consultar_logs, init_db
#instanciamos el objeto app y el argumento que le indica a flask donde buscar recursos
app = Flask(__name__)

#utilizamos el decorador para vincular una URL a las funciones, utilizamos el metodo POST
@app.route("/auth/token", methods=["POST"])
#funcion encargada de obtener los tokens de los servicios
def obtener_token():
    #recibe el json enviado por el cliente y lo convierte a un diccionario
    data = request.get_json()
    #accedemos al campo de service_name que se encuentra dentro del diccionario 
    service_name = data["service_name"]
    #guardamos el token generado en una variable donde se llama a la funcion que recibe como argumento el nombre del servicio
    token = generar_token(service_name)
    #se retorna el token generado al servicio mediante jsonify
    return jsonify({"token": token}), 200

#ruta para recibir y almacenar logs enviados por los servicios
@app.route("/logs", methods=["POST"])
#funcion encargada del manejo de los tokens de los servicios (verifica y guarda los tokens)
def manejo_logs():
    #extraer el token que el servicio mando
    token = request.headers.get("Authorization")
    #verificamos el token obtenido del servicio y lo guardamos en una variable
    token_verificado = verificar_token(token)
    #si el token falla en la verificacion entonces se retorna error
    if token_verificado == None:
        return jsonify({"error": "Quien sos, bro?"}), 401
    #recibimos los logs como un diccionario de python y lo guardamos en la variable
    logs_list = [request.get_json()]
    #llamamos a la funcion para insertar la lista de logs dentro de la base de datos
    log_guardado = insertar_logs(logs_list)
    #verificacion por si los logs no llegaron a guardarse
    if not log_guardado:
        #retorna mensaje de error con error 500 error del servidor
        return jsonify({"error": "No se pudieron guardar los logs"}), 500
    #si no hay nada en la variable save_logs entonces se retorna un mensaje de error 
    return jsonify({"mensaje": "logs guardados correctamente"}), 201

#ruta para consultar y visualizar los logs almacenados, acepta filtros de fecha opcionales
@app.route("/logs", methods=["GET"])
#funcion encargada de mostrar los logs en formato JSON para monitoreo
def obtener_logs():
    #extrae los parametros de la query de la url
    #fecha del inicio del evento
    occurred_at_start = request.args.get("occurred_at_start")
    #fecha fin del evento
    occurred_at_end = request.args.get("occurred_at_end")
    #fecha inicio de recepcion
    received_at_start = request.args.get("received_at_start")
    #fecha fin de recepcion
    received_at_end = request.args.get("received_at_end")
    # Consultar logs filtrando por rangos de fecha de ocurrencia y recepción
    traer_logs = consultar_logs(occurred_at_start,occurred_at_end,received_at_start,received_at_end)
    #verificacion por si los logs no se pudieron consultar 
    if traer_logs is None:
        #retornamos mensaje de error interno del servidor
        return jsonify({"error": "No se pudieron obtener los logs"}), 500
    #retornamos un JSON con los logs
    return jsonify({"logs": traer_logs}), 200

#punto de entrada de la aplicación
if __name__ == "__main__":
    #inicia la base de datos creando las tablas
    init_db()
    #reinicia el servidor automaticamente cuando se realiza un cambio en el codigo
    app.run(debug=True)