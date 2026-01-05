from config.connection import get_connection

def get_reclasificaciones_balance():
    conn = get_connection()
    if not conn:
        return [], []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLANFIN.EDSA.ReclasificacionesBalance where periodoid = 202409")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return rows, columns

def get_reclasificaciones_resultado():
    conn = get_connection()
    if not conn:
        return [], []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLANFIN.EDSA.ReclasificacionesResultado where periodoid = 202409")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return rows, columns
