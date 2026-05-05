def generar_informe(data):

    obs = "\n- ".join(data["observaciones"]) if data["observaciones"] else "Sin observaciones"

    return f"""
INFORME TÉCNICO

Docente: {data.get('nombre')}
CI: {data.get('ci')}

Total de horas: {data.get('total_horas', 'N/D')}

Observaciones:
- {obs}

Conclusión:
{"FAVORABLE" if not data["observaciones"] else "CON OBSERVACIONES"}
"""
