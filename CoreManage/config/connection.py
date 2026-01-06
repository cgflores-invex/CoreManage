import pyodbc
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")

# Conexión a SQL Server
def get_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            "Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        print("✅ Conexión exitosa a SQL Server")
        return conn
    except Exception as e:
        print("❌ Error de conexión:", e)
        return None

