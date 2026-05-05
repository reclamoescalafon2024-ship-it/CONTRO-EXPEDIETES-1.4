def generar_informe(data):

    obs = "\n- ".join(data["observaciones"]) if data["observaciones"] else "Sin observaciones"

    return f"""
INFORME TÉCNICO

Docente: {data.get('nombre')}
CI: {data.get('ci')}

Horas expediente: {data.get('horas_pdf')}
Horas sistema: {data.get('horas_excel', 'N/D')}

Observaciones:
- {obs}

Conclusión:
{"FAVORABLE" if not data["observaciones"] else "OBSERVADO"}
"""
