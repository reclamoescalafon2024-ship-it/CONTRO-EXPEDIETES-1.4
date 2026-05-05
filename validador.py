def validar_datos(data):

    resultado = data.copy()
    resultado["observaciones"] = []

    # ✔ total horas
    if data["total_horas"] > 50:
        resultado["observaciones"].append("Supera el máximo de 50 horas")

    # ✔ múltiples organismos
    if len(data["horas"]) > 1:
        resultado["multiempleo"] = True
    else:
        resultado["multiempleo"] = False

    # ✔ control de consistencia textual
    if "no existe interferencia" not in data["texto"].lower():
        resultado["observaciones"].append("No consta validación de contralor en expediente")

    return resultado
