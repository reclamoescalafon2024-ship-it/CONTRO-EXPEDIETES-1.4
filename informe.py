def generar_informe(data):

    obs = "\n- ".join(data.get("observaciones", [])) if data.get("observaciones") else "Sin observaciones"

    return f"""
INFORME TÉCNICO

Docente: {data.get('nombre')}
CI: {data.get('ci')}

Total horas: {data.get('total_horas', 'N/D')}

Observaciones:
- {obs}

Conclusión:
{"FAVORABLE" if not data.get("observaciones") else "OBSERVADO"}
"""
