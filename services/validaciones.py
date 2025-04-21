def validar_deposito_fondo(fila, config):
    """
    fila: tuple con los datos del depósito (espera mínimo 13 columnas)
    config: dict con claves 'cuenta_origen', 'descripcion', 'forma_pago', 'importe'
    
    return: lista booleana por columna de validación (solo las columnas validadas)
    """
    validaciones = []

    # Columna 4: Cuenta Origen
    validaciones.append(fila[4] == config["cuenta_origen"])

    # Columna 5: Cuenta Desc
    validaciones.append(fila[5] == config["descripcion"])

    

    # Columna 8: Importe
    try:
        importe = float(fila[8])
    except:
        importe = 0.0
    validaciones.append(abs(importe - config["importe"]) < 0.01)

    # Columna 9: Forma de Pago
    validaciones.append(fila[9] == config["forma_pago"])

    #Columna 12:Estatus
    validaciones.append(fila[12] == "CONCLUIDO")

    return validaciones
