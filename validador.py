def validar_datos(data_pdf, df_horas, df_dsf):

    resultado = {
        "ci": data_pdf.get("ci"),
        "nombre": data_pdf.get("nombre"),
        "horas_pdf": data_pdf.get("horas_pdf", 0),
        "observaciones": []
    }

    if not resultado["ci"]:
        resultado["observaciones"].append("No se pudo extraer CI")
        return resultado

    ci = resultado["ci"].replace("-", "")

    if "CI" not in df_horas.columns or "HORAS" not in df_horas.columns:
        resultado["observaciones"].append("Excel horas mal formado")
        return resultado

    df_horas["CI"] = df_horas["CI"].astype(str).str.replace("-", "")
    docente = df_horas[df_horas["CI"] == ci]

    if docente.empty:
        resultado["observaciones"].append("No aparece en Excel")
        return resultado

    horas_excel = docente["HORAS"].sum()
    resultado["horas_excel"] = horas_excel

    if horas_excel != resultado["horas_pdf"]:
        resultado["observaciones"].append("Diferencia PDF vs Excel")

    if horas_excel > 50:
        resultado["observaciones"].append("Supera 50 horas")

    df_dsf["CI"] = df_dsf["CI"].astype(str).str.replace("-", "")

    if ci not in df_dsf["CI"].values:
        resultado["observaciones"].append("Sin DSF")

    return resultado
