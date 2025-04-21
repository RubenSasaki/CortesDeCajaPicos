# db/conexion.py
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    try:
        conexion = pyodbc.connect(
            f'DRIVER={{ODBC Driver 18 for SQL Server}};'
            f'SERVER={os.getenv("SQL_SERVER")},{os.getenv("SQL_PORT")};'
            f'DATABASE={os.getenv("SQL_DATABASE")};'
            f'UID={os.getenv("SQL_USER")};'
            f'PWD={os.getenv("SQL_PASSWORD")};'
            f'Encrypt=yes;TrustServerCertificate=yes;'
        )
        return conexion
    except pyodbc.Error as e:
        print(f"Error de conexión: {e}")
        return None



