def parse_hora(hora):
    h, m = hora.split(":")
    return int(h) * 60 + int(m)


def hay_superposicion(horarios):
    conflictos = []

    for i in range(len(horarios)):
        for j in range(i + 1, len(horarios)):

            h1 = horarios[i]
            h2 = horarios[j]

            if h1["dia"] == h2["dia"]:

                ini1 = parse_hora(h1["inicio"])
                fin1 = parse_hora(h1["fin"])

                ini2 = parse_hora(h2["inicio"])
                fin2 = parse_hora(h2["fin"])

                if ini1 < fin2 and ini2 < fin1:
                    conflictos.append((h1, h2))

    return conflictos


def validar_datos(data):

    horarios = data.get("horarios", [])

    total_horas = 0

    for h in horarios:
        try:
            ini = parse_hora(h["inicio"])
            fin = parse_hora(h["fin"])
            total_horas += (fin - ini) / 60
        except:
            continue

    conflictos = hay_superposicion(horarios)

    observaciones = []

    if conflictos:
        observaciones.append("Superposición horaria detectada")

    if total_horas > 48:
        observaciones.append("Exceso de carga horaria (>48 horas)")

    resultado = {
        "nombre": data.get("nombre"),
        "ci": data.get("ci"),
        "total_horas": round(total_horas, 2),
        "conflictos": conflictos,
        "observaciones": observaciones,
        "multiempleo": False,
        "organismos": ["ANEP"]  # podés mejorar esto después
    }

    return resultado
