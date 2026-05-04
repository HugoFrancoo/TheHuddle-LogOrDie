#libreria para generar y verificar tokens JWT
import jwt
#libreria para acceder a las variables de entorno del sistema operativo
import os
#lee el valor de la variable almacenada en .env para utilizarla
SECRET_KEY='ba44edf3b4f49a3650ef41eb1afcae841de3545a421e490a34fbeb6c4b0753aa'
#funcion encargada de generar los tokens para cada servicio
def generar_token(service_name):
    #generamos el token JWT con el nombre del servicio firmado con la clave secreta
    token = jwt.encode({'service_name': service_name}, SECRET_KEY, algorithm='HS256')
    #se retorna el token generado
    return token

def verificar_token(token):
    try:
        #se decodifica el token para poder verificarlo con la SECRET KEY y se le indica el algoritmo utilizado para verificar la firma 
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        #se retorna el nombre del servicio al que corresponde el token 
        return payload["service_name"]
        #excepcion que evalua si la firma no coincide o el token es invalido
    except jwt.InvalidTokenError as e:
        print(e)
        return None
        #cualquier otro error inesperado
    except Exception as e:
        print(f"Hubo un error: {e}")
        return None