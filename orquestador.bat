@echo off
cd C:\Users\Hugo Franco\Desktop\TheHuddle-LogOrDie

start "game-service" cmd /k python "services\game-service.py"
start "matchmaking-service" cmd /k python "services\matchmaking-service.py"
start "anticheat-service" cmd /k python "services\anticheat-service.py"
start "Servidor Flask" cmd /k python "server\app.py"
pause