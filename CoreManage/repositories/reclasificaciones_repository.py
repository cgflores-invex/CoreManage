from config.connection import get_connection

# -------------------- CONSULTAS --------------------
def get_reclasificaciones_balance():
    conn = get_connection()
    if not conn:
        return [], []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLANFIN.EDSA.ReclasificacionesBalance order by PeriodoId desc")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return rows, columns

def get_reclasificaciones_resultado():
    conn = get_connection()
    if not conn:
        return [], []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLANFIN.EDSA.ReclasificacionesResultado order by PeriodoId desc")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return rows, columns

# -------------------- INSERTAR --------------------
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

def insertar_resultado(data):
    conn = get_connection()
    if not conn:
        print("❌ No se pudo conectar a la base de datos")
        return
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO PLANFIN.EDSA.ReclasificacionesResultado
            (DataAreaId, PeriodoId, Descripcion, NumCentroCostos, 
             NumIntercompania, NumLineaNegocio, NumDeducible, 
             NumProyecto, Reclasificacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        print("✅ Registro insertado correctamente")
    except Exception as e:
        conn.rollback()
        print("❌ Error al insertar:", e)
    finally:
        cursor.close()
        conn.close()

# -------------------- ELIMINAR --------------------
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

def eliminar_resultado(dataareaid, periodoid, reclasificacion):
    conn = get_connection()
    if not conn:
        print("❌ No se pudo conectar a la base de datos")
        return

    cursor = conn.cursor()
    try:
        # Limpiar y convertir tipos
        dataareaid = str(dataareaid).strip()
        periodoid = int(periodoid)
        reclasificacion = float(reclasificacion)

        # Usar ROUND para coincidir decimal, y limpiar DataAreaId
        cursor.execute("""
            DELETE FROM PLANFIN.EDSA.ReclasificacionesResultado
            WHERE LTRIM(RTRIM(DataAreaId)) = ? 
              AND PeriodoId = ? 
              AND ROUND(Reclasificacion, 2) = ROUND(?, 2)
        """, (dataareaid, periodoid, reclasificacion))

        conn.commit()

        if cursor.rowcount == 0:
            print(f"⚠️ No se encontró ningún registro para eliminar: {dataareaid}, {periodoid}, {reclasificacion}")
        else:
            print(f"✅ Registro eliminado correctamente: {dataareaid}, {periodoid}, {reclasificacion}")

    except Exception as e:
        conn.rollback()
        print("❌ Error al eliminar:", e)
    finally:
        cursor.close()
        conn.close()





