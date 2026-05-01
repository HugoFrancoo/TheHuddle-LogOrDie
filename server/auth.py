import jwt
import datetime
import os
from dotenv import load_dotenv

#generamos una secret key unica para poder verificar la autenticidad de las firmas del token
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def generar_token(service_name):
    #generamos el token unico mediante JWT datetime.utcnow obtiene la fecha y hora actual y timedelta representa la cantidad de tiempo
    token = jwt.encode({'service_name': service_name,"exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, SECRET_KEY, algorithm='HS256')
    return token

def verificar_token(token):
    try:
        #se decodifica el token para poder verificarlo con la SECRET KEY y se le indica el algoritmo utilizado para verificar la firma 
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        #se retorna el nombre del servicio al que corresponde el token 
        return payload["service_name"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        print(e)
        return None
    except Exception as e:
        print(f"Hubo un error: {e}")
        return None