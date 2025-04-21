import json
from pathlib import Path
from typing import Dict, List


class Config:    
    _sucursales: List[Dict] = []
    _config = None
    _icons_base_path = "resources/icons"
    
    @classmethod
    def initialize(cls):
        """Carga la configuración inicial"""
        # Cargar configuración general
        config_path = Path("config/settings.json")
        if config_path.exists():
            with open(config_path) as f:
                cls._config = json.load(f)
                
    @classmethod
    def get_icon(cls, name: str, theme: str = "light") -> str:
        """Obtiene la ruta de un icono"""
        icon_path = Path(cls._icons_base_path) / theme / f"{name}.svg"
        if not icon_path.exists():
            icon_path = Path(cls._icons_base_path) / "default" / f"{name}.svg"
        return str(icon_path)
    
    
    @classmethod
    def cargar_sucursales(cls):
        """Carga las sucursales desde el archivo JSON"""
        try:
            ruta = Path(__file__).parent / "config" / "sucursales.json"
            with open(ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            cls._sucursales = datos.get('sucursales', [])
        except Exception as e:
            raise RuntimeError(f"Error cargando sucursales: {str(e)}")

    @classmethod
    def obtener_sucursales_activas(cls) -> List[Dict]:
        """Devuelve solo sucursales activas"""
        return [s for s in cls._sucursales if s.get('activa', False)]

    @classmethod
    def obtener_fondo_fijo(cls, codigo: str) -> float:
        """Obtiene el fondo fijo por código de sucursal"""
        for sucursal in cls._sucursales:
            if sucursal['codigo'] == codigo:
                return sucursal.get('fondo_fijo', 0.0)
        return 0.0

