import platform
import socket
import datetime
import os

print("=== INFORMACIÓN DEL SISTEMA ===")
print(f"Hostname: {socket.gethostname()}")
print(f"Sistema operativo: {platform.system()}")
print(f"Versión: {platform.version()}")
print(f"Arquitectura: {platform.machine()}")
print(f"Python: {platform.python_version()}")
print(f"Fecha: {datetime.datetime.now()}")

usuario = os.getenv("PARAM_USUARIO", "desconocido")
print(f"Usuario recibido: {usuario}")

print("Programa ejecutado correctamente")
