def generar_informe(data):

    horas_detalle = ""

    if "horas" in data:
        for k, v in data["horas"].items():
            horas_detalle += f"- {k}: {v} hs\n"

    obs = "\n- ".join(data.get("observaciones", [])) if data.get("observaciones") else "Sin observaciones"

    return f"""
INFORME TÉCNICO

Docente: {data.get('nombre')}
CI: {data.get('ci')}

Detalle de carga horaria:
{horas_detalle}

Total: {data.get('total_horas', 'N/D')} horas

Observaciones:
- {obs}

Conclusión:
{"FAVORABLE" if not data.get("observaciones") else "OBSERVADO"}
"""
