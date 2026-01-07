from repositories.reclasificaciones_repository import (
    get_reclasificaciones_balance,
    get_reclasificaciones_resultado,
    insertar_balance as repo_insertar_balance,
    eliminar_balance as repo_eliminar_balance,
    insertar_resultado as repo_insertar_resultado,
    eliminar_resultado as repo_eliminar_resultado,

)

# Listar datos
def listar_balance():
    return get_reclasificaciones_balance()

def listar_resultado():
    return get_reclasificaciones_resultado()

# Insertar datos
def insertar_balance_service(data):
    repo_insertar_balance(data)

def insertar_resultado_service(data):
    repo_insertar_resultado(data)

# Eliminar datos
def eliminar_balance_service(dataareaid, periodoid, reclasificacion):
    repo_eliminar_balance(dataareaid, periodoid, reclasificacion)

def eliminar_resultado_service(dataareaid, periodoid, reclasificacion):
    repo_eliminar_resultado(dataareaid, periodoid, reclasificacion)
