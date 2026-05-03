#libreria para generar y verificar tokens JWT
import jwt
#libreria para acceder a las variables de entorno del sistema operativo
import os
#libreria para cargar las variables de entorno desde el archivo .env
from dotenv import load_dotenv

#busca el archivo .env para de ahi extraer la key 
load_dotenv()
#lee el valor de la variable almacenada en .env para utilizarla
SECRET_KEY = os.getenv("SECRET_KEY")
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