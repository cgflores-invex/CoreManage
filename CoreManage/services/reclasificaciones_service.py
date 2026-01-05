from repositories.reclasificaciones_repository import get_reclasificaciones_balance, get_reclasificaciones_resultado

def listar_balance():
    return get_reclasificaciones_balance()

def listar_resultado():
    return get_reclasificaciones_resultado()
