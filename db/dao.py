from .models import Sucursal
from .conexion import DatabaseManager

class BranchDAO:
    @classmethod
    def get_all_active(cls) -> list[Sucursal]:
        query = """
            SELECT id, codigo, nombre, fondo_fijo 
            FROM sucursales 
            WHERE activa = 1
        """
        
        sucursales = []
        with DatabaseManager().get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                sucursales.append(
                    Sucursal(
                        id=row[0],
                        codigo=row[1],
                        nombre=row[2],
                        fondo_fijo=row[3]
                    )
                )
        return sucursales

    @classmethod
    def get_by_code(cls, codigo: str) -> Sucursal:
        query = """
            SELECT id, codigo, nombre, fondo_fijo 
            FROM sucursales 
            WHERE codigo = ?
        """
        
        with DatabaseManager().get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (codigo,))
            result = cursor.fetchone()
            
        if result:
            return Sucursal(
                id=result[0],
                codigo=result[1],
                nombre=result[2],
                fondo_fijo=result[3]
            )
        return None
