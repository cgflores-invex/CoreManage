from config.connection import get_connection
from repositories.reclasificaciones_repository import (
    get_reclasificaciones_balance,
    get_reclasificaciones_resultado,
    insertar_balance as repo_insertar_balance,
    eliminar_balance as repo_eliminar_balance
)

# Listar datos
def listar_balance():
    return get_reclasificaciones_balance()

def listar_resultado():
    return get_reclasificaciones_resultado()

# Insertar datos
def insertar_balance_service(data):
    repo_insertar_balance(data)

# Eliminar datos
def eliminar_balance_service(dataareaid, periodoid, reclasificacion):
    repo_eliminar_balance(dataareaid, periodoid, reclasificacion)
