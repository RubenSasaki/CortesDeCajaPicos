# config/fondos.py
fondos_fijos = {
    "01MATRIZ": 2361.55,
    "02IXCOTEL": 6556.00,
    "03SERRANO": 7018.86,
    "04MONTOYA": 3500.00,
    "05RIVERAS": 2656.00,
    "06FERRO": 2000.00,
    "07RIOS": 2000.00,
    "08VOLCANES": 2000.00,
    "09XOXO": 2000.00
}

def get_fondo_fijo(sucursal):
    return fondos_fijos.get(sucursal, 0.0)


