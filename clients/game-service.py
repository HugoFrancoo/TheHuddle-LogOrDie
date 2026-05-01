import requests
import random 

response = requests.post(
    "http://localhost:5000/auth/token",
    json={"service_name": "game-service"}
)

data = response.json()
token = data["token"]