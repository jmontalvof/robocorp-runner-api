import os

nombre = os.getenv("PARAM_NOMBRE", "Jorge")

print(f"Hola {nombre}, tarea ejecutada correctamente desde Robocorp Runner API")
