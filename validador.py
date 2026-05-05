from datetime import datetime

def parse_hora(h):
    return datetime.strptime(h, "%H:%M")

def hay_superposicion(horarios):

    for i in range(len(horarios)):
        for j in range(i+1, len(horarios)):

            h1 = horarios[i]
            h2 = horarios[j]

            if h1["dia"] != h2["dia"]:
                continue

            inicio1 = parse_hora(h1["inicio"])
            fin1 = parse_hora(h1["fin"])
            inicio2 = parse_hora(h2["inicio"])
            fin2 = parse_hora(h2["fin"])

            if inicio1 < fin2 and inicio2 < fin1:
                return True

    return False


def validar_datos(data):

    resultado = {
        "ci": data["ci"],
        "nombre": data["nombre"],
        "observaciones": []
    }

    horarios = data["horarios"]

    # ✔ sin horarios
    if not horarios:
        resultado["observaciones"].append("No se detectaron horarios en el expediente")
        return resultado

    # ✔ superposición
    if hay_superposicion(horarios):
        resultado["observaciones"].append("Se detecta superposición horaria")

    # ✔ total horas
    total_horas = 0
    for h in horarios:
        inicio = parse_hora(h["inicio"])
        fin = parse_hora(h["fin"])
        total_horas += (fin - inicio).seconds / 3600

    resultado["total_horas"] = total_horas

    if total_horas > 50:
        resultado["observaciones"].append("Supera el máximo de horas permitido")

    # ✔ declaración inconsistente
    if not data["declara_otros"] and len(horarios) > 1:
        resultado["observaciones"].append("Posible inconsistencia en declaración de vínculos")

    return resultado
