from dataclasses import dataclass

@dataclass
class Sucursal:
    id_sucursal: int
    codigo_suc: str
    nombre_suc: str
    fondo: float
    activa: bool = True
