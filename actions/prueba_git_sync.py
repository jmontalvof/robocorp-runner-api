import os
from datetime import datetime

print("Prueba OK desde Git Sync")
print("Fecha:", datetime.now())
print("Entorno:", os.getenv("PARAM_ENTORNO", "sin entorno"))
print("Version:", os.getenv("PARAM_VERSION", "sin version"))
