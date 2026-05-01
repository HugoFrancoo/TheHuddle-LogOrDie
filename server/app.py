#importamos la clase Flask de flask para poder instanciar objetos apartir de el
from flask import Flask, request, jsonify
#importamos las funciones para generar token y para verificarlas
from auth import generar_token, verificar_token
#importamos la funcion insertar_logs para almacenar la informacion en nuestra base de datos
from database import insertar_logs, consultar_logs
#instanciamos el objeto app y el argumento que le indica a flask donde buscar recursos
app = Flask(__name__)

#utilizamos el decorador para vincular una URL a las funciones, utilizamos el methodo POST
@app.route("/auth/token", methods=["POST"])
#funcion encargada de obtener los tokens de los servicios
def get_token():
    #recibe el json enviado por el cliente y lo convierte a un diccionario
    data = request.get_json()
    #accedemos al campo de service_name que se encuentra dentro del diccionario 
    service_name = data["service_name"]
    #guardamos el token generado en una variable donde se llama a la funcion que recibe como argumento el nombre del servicio
    token = generar_token(service_name)
    #se retorna el token generado al servicio mediante jsonify
    return jsonify({"token": token}), 200

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
    save_logs = insertar_logs(logs_list)
    #retornamos un JSON con un mensaje de guardado correctamente 
    return jsonify({"mensaje": "logs guardados correctamente"}), 201

@app.route("/logs", methods=["GET"])
#funcion encargada de mostrar los logs en un JSON
def obtener_logs():
    #llamamos a la funcion para mostrar los logs
    traer_logs = consultar_logs()
    #retornamos un JSON con los logs
    return jsonify({"logs": traer_logs}), 200

if __name__ == "__main__":
    app.run(debug=True)