from config.connection import get_connection

def get_reclasificaciones_balance():
    conn = get_connection()
    if not conn:
        return [], []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLANFIN.EDSA.ReclasificacionesBalance")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return rows, columns

def get_reclasificaciones_resultado():
    conn = get_connection()
    if not conn:
        return [], []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLANFIN.EDSA.ReclasificacionesResultado")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return rows, columns

def insertar_balance(data):
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO PLANFIN.EDSA.ReclasificacionesBalance
            (DataAreaId,PeriodoId,Descripcion,NumIntercompania,NumLineaNegocio,NumProyecto,Reclasificacion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
    except Exception as e:
        print("❌ Error al insertar:", e)
    finally:
        cursor.close()
        conn.close()

def eliminar_balance(dataareaid, periodoid, reclasificacion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM PLANFIN.EDSA.ReclasificacionesBalance 
        WHERE DataAreaId = ? AND PeriodoId = ? AND Reclasificacion = ?
    """, (dataareaid, periodoid, reclasificacion))
    conn.commit()
    cursor.close()
    conn.close()

