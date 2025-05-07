# services/consulta_service.py
from db.conexion import obtener_conexion

def run_query(query):
    datos = []
    con = obtener_conexion()
    if con:
        cursor = con.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            datos.append((row[0], float(row[1])))
        cursor.close()
        con.close()
    return datos

# === Consultas Generales por Tipo ===
def consulta_generica(query_template, **params):
    query = query_template.format(**params)
    return run_query(query)

QUERY_TEMPLATES = {
    "facturas": """
        SELECT b.FormaCobro1, SUM(a.Importe + a.Impuestos - ISNULL(a.AnticiposFacturados, 0))
        FROM Venta a
        INNER JOIN VentaCobro b ON a.ID = b.ID
        WHERE a.Mov = 'Factura' AND a.FechaEmision = '{fecha}'
        AND a.Sucursal = {sucursal} AND a.DineroCtaDinero = '{cuenta}'
        AND a.Condicion NOT IN (
            '1 DIAS','10 DIAS','120 DIAS','15 DIAS','2 DIAS','20 DIAS','25 DIAS','3 DIAS','30 DIAS',
            '4 DIAS','40 DIAS','45 DIAS','5 DIAS','6 DIAS','60 DIAS','8 DIAS','9 DIAS','90 DIAS')
        GROUP BY b.FormaCobro1
    """,
    "notas": """
        SELECT b.FormaCobro1, SUM(a.Importe + a.Impuestos)
        FROM Venta a
        INNER JOIN VentaCobro b ON a.ID = b.ID
        WHERE a.Mov = 'Nota' AND a.Estatus IN ('Concluido', 'Procesar')
        AND a.FechaEmision = '{fecha}' AND a.Sucursal = {sucursal}
        AND a.DineroCtaDinero = '{cuenta}'
        GROUP BY b.FormaCobro1
    """,
    "cobranza": """
        SELECT FormaCobro,
            SUM(CASE WHEN Mov = 'Devolucion' THEN (Importe * -1 + Impuestos * -1)
                     ELSE (Importe + Impuestos) END)
        FROM CXC
        WHERE Mov IN ('Cobro', 'Anticipo', 'Anticipo N', 'Cobro Anticipo', 'Devolucion')
        AND FechaEmision = '{fecha}' AND Sucursal = {sucursal}
        AND Estatus IN ('Concluido', 'Pendiente')
        AND CtaDinero = '{cuenta}'
        GROUP BY FormaCobro
    """,
    "devoluciones": """
        SELECT b.FormaCobro1, SUM((a.Importe + a.Impuestos) * -1)
        FROM Venta a
        INNER JOIN VentaCobro b ON a.ID = b.ID
        WHERE a.Mov IN ('Devolucion Venta', 'Cancelacion Factura')
        AND a.FechaEmision = '{fecha}' AND a.Sucursal = {sucursal}
        AND a.DineroCtaDinero = '{cuenta}'
        AND a.Estatus = 'Concluido'
        AND a.Condicion NOT IN (
            '1 DIAS','10 DIAS','120 DIAS','15 DIAS','2 DIAS','20 DIAS','25 DIAS','3 DIAS','30 DIAS',
            '4 DIAS','40 DIAS','45 DIAS','5 DIAS','6 DIAS','60 DIAS','8 DIAS','9 DIAS','90 DIAS')
        GROUP BY b.FormaCobro1
    """,
    "corte": """
        SELECT d.FormaPago, SUM(d.Importe)
        FROM Dinero m
        INNER JOIN DineroD d ON m.ID = d.ID
        WHERE m.Mov = 'Corte Caja' AND m.Estatus = 'CONCLUIDO'
        AND m.FechaEmision = '{fecha}' AND m.Sucursal = {sucursal}
        GROUP BY d.FormaPago
    """
}

def obtener_facturas(fecha, sucursal, cuenta):
    return consulta_generica(QUERY_TEMPLATES['facturas'], fecha=fecha, sucursal=sucursal, cuenta=cuenta)

def obtener_notas(fecha, sucursal, cuenta):
    return consulta_generica(QUERY_TEMPLATES['notas'], fecha=fecha, sucursal=sucursal, cuenta=cuenta)

def obtener_cobranza(fecha, sucursal, cuenta):
    return consulta_generica(QUERY_TEMPLATES['cobranza'], fecha=fecha, sucursal=sucursal, cuenta=cuenta)

def obtener_devoluciones(fecha, sucursal, cuenta):
    return consulta_generica(QUERY_TEMPLATES['devoluciones'], fecha=fecha, sucursal=sucursal, cuenta=cuenta)

def obtener_corte(fecha, sucursal):
    return consulta_generica(QUERY_TEMPLATES['corte'], fecha=fecha, sucursal=sucursal, cuenta="")

def obtener_depositos(fecha, sucursal):
    query = f"""
        SELECT D.Mov, D.MovID, D.FechaEmision, M.TipoCambio, CD.CtaDinero, CD.Descripcion AS CuentaOrigen,
               D.Origen, D.OrigenID, D.Importe, D.FormaPago, D.Referencia,
               D.Moneda, D.Estatus
        FROM Dinero D
        LEFT JOIN CtaDinero CD ON D.CtaDinero = CD.CtaDinero
        LEFT JOIN Mon M ON D.Moneda = M.Moneda
        WHERE D.Mov = 'Deposito Caja'
        AND D.Sucursal = {sucursal}
        AND D.FechaEmision = '{fecha}'
        ORDER BY D.FechaEmision DESC
    """
    con = obtener_conexion()
    resultados = []
    if con:
        cursor = con.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            resultados.append(tuple(row))
        cursor.close()
        con.close()
    return resultados

def obtener_corte_z(fecha: str, sucursal: str):
    query = f"EXEC xpCorteZPicos '{fecha}', '{sucursal}'"
    con = obtener_conexion()
    if not con:
        print("[CorteZ] No se pudo conectar a la base de datos.")
        return {}

    try:
        cursor = con.cursor()
        cursor.execute(query)

     # AVANZAR hasta que haya columnas reales
        while cursor.description is None and cursor.nextset():
            pass

        if cursor.description is None:
            print(f"[CorteZ] No se devolvieron resultados. Verifica fecha ({fecha}) y sucursal ({sucursal})")
            return {}

        columnas = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        con.close()

        secciones = {
            1: "apertura",
            2: "movimientos",
            3: "corte",
            4: "diferencia",
            5: "ventas_credito"
        }

        datos = {nombre: [] for nombre in secciones.values()}
        idx_cual = columnas.index("Cual")

        for fila in rows:
            cual = fila[idx_cual]
            if cual in secciones:
                datos[secciones[cual]].append(fila)

        return {"columnas": columnas, "datos": datos}

    except Exception as e:
        print(f"[CorteZ] ERROR al ejecutar el SP: {e}")
        return {}
