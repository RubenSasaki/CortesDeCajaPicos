# services/resumen_service.py
def calcular_resumen(fecha, sucursal, cuenta, fondo_fijo, formas, funciones_consulta):
    def suma_map(datos):
        mapa = {}
        for forma, total in datos:
            mapa[forma] = mapa.get(forma, 0.0) + total
        return mapa

    # Obtener totales por tipo
    total_facturas = suma_map(funciones_consulta['facturas'](fecha, sucursal, cuenta))
    total_notas = suma_map(funciones_consulta['notas'](fecha, sucursal, cuenta))
    total_cobranza = suma_map(funciones_consulta['cobranza'](fecha, sucursal, cuenta))
    total_devoluciones = suma_map(funciones_consulta['devoluciones'](fecha, sucursal, cuenta))
    total_corte = suma_map(funciones_consulta['corte'](fecha, sucursal))

    # Acumulador de revisión
    total_revision = {}
    for dic in [total_facturas, total_notas, total_cobranza, total_devoluciones]:
        for k, v in dic.items():
            total_revision[k] = total_revision.get(k, 0.0) + v
    total_revision['Fondo Fijo'] = fondo_fijo

    resumen = []
    for forma in formas:
        corte = total_corte.get(forma, 0.0)
        revision = total_revision.get(forma, 0.0)
        diferencia = round(corte - revision, 2)
        resumen.append((forma, corte, revision, diferencia))

    total_corte_sum = sum(total_corte.values())
    total_revision_sum = sum(total_revision.values())
    diferencia_total = round(total_corte_sum - total_revision_sum, 2)
    resumen.append(("TOTALES", total_corte_sum, total_revision_sum, diferencia_total))

    return resumen


