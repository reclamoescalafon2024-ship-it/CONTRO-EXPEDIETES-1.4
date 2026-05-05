import fitz
import re

def extraer_datos_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")

    texto = ""
    for page in doc:
        texto += page.get_text()

    ci = re.search(r"\d{7,8}-?\d", texto)
    ci = ci.group() if ci else None

    nombre = re.search(r"Nombre Titular:\s*(.+)", texto)
    nombre = nombre.group(1).strip() if nombre else "No detectado"

    horas = re.findall(r"(\d{1,2})hs", texto)
    horas = [int(h) for h in horas]

    return {
        "ci": ci,
        "nombre": nombre,
        "horas_pdf": sum(horas)
    }
