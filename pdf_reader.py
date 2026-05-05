import fitz
import re
import unicodedata


def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    texto = texto.replace("\n", " ")
    return texto


def extraer_datos_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")

    texto_raw = ""
    for page in doc:
        texto_raw += page.get_text()

    texto = normalizar(texto_raw)

    # -------------------------
    # CI
    # -------------------------
    ci_match = re.search(r"\d{7,8}-?\d", texto)
    ci = ci_match.group() if ci_match else None

    # -------------------------
    # NOMBRE
    # -------------------------
    nombre = "No detectado"

    m = re.search(r"nombre titular:\s*([a-z\s]+)", texto)
    if m:
        nombre = m.group(1).strip().title()
    else:
        m = re.search(r"docente\s+([a-z\s]+)", texto)
        if m:
            nombre = m.group(1).strip().title()

    # -------------------------
    # HORAS POR ORGANISMO
    # -------------------------
    horas = {}

    patron = r"(cfe|direccion general de educacion secundaria).*?(\d{1,2})\s*hs"

    for match in re.findall(patron, texto):
        org = match[0]
        h = int(match[1])

        if "cfe" in org:
            horas["CFE"] = horas.get("CFE", 0) + h
        elif "secundaria" in org:
            horas["DGES"] = horas.get("DGES", 0) + h

    # -------------------------
    # TOTAL
    # -------------------------
    total = sum(horas.values())

    return {
        "ci": ci,
        "nombre": nombre,
        "horas": horas,
        "total_horas": total,
        "texto": texto_raw
    }
