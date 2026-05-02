# 🐧 LogOrDie — Sistema de Logging Distribuido

Sistema de logging distribuido donde múltiples servicios simulados envían logs a un servidor central que los valida, almacena y expone para consulta.

---

## 🛠️ Tecnologías

- Python + Flask
- PostgreSQL
- JWT (PyJWT)
- psycopg2

---

## 📁 Estructura del proyecto

LogOrDie/
├── server/
│   ├── app.py
│   ├── auth.py
│   └── database.py
├── services/
│   ├── game-service.py
│   ├── matchmaking-service.py
│   └── anticheat-service.py
├── diagramas/
│   └── flujo.drawio
├── .env
├── .gitignore
├── requirements.txt
└── README.md

---

## ⚙️ Instalación

```bash
# Clonar el repositorio
git clone <url>

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## 🔑 Variables de entorno

Creá un archivo `.env` en la raíz con:

SECRET_KEY=tu_clave_secreta

---

## 🗄️ Base de datos

Creá la base de datos en PostgreSQL:

```sql
CREATE DATABASE LogOrDIe;
```

La tabla se crea automáticamente al arrancar el servidor.

---

## 🚀 Cómo correrlo

**Terminal 1 — Servidor:**
```bash
cd server
python app.py
```

**Terminal 2, 3, 4 — Servicios:**
```bash
cd services
python game-service.py
python matchmaking-service.py
python anticheat-service.py
```

---

## 📡 Endpoints

### `POST /auth/token`
Solicita un JWT para autenticar el servicio.

**Body:**
```json
{
    "service_name": "game-service"
}
```

**Respuesta:**
```json
{
    "token": "eyJhbGci..."
}
```

---

### `POST /logs`
Envía un log al servidor. Requiere JWT en el header.

**Header:**
Authorization: <token>
**Body:**
```json
{
    "occurred_at": "2026-05-02T23:13:00",
    "service": "game-service",
    "severity": "ERROR",
    "message": "Jugador #1234 desconectado abruptamente"
}
```

**Respuesta:**
```json
{
    "mensaje": "logs guardados correctamente"
}
```

---

### `GET /logs`
Consulta los logs almacenados con filtros opcionales.

**Filtros opcionales:**
?occurred_at_start=2026-05-01T00:00:00
?occurred_at_end=2026-05-02T23:59:59
?received_at_start=2026-05-01T00:00:00
?received_at_end=2026-05-02T23:59:59

**Respuesta:**
```json
{
    "logs": [...]
}
```

---

## 🔐 Autenticación

El sistema usa JWT. Cada servicio solicita su token en `POST /auth/token` y lo incluye en el header de cada request a `POST /logs`. Si el token es inválido el servidor responde:

```json
{
    "error": "Quien sos, bro?"
}
```