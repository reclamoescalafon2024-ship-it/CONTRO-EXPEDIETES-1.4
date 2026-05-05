import fitz
import re

def extraer_datos_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")

    texto = ""
    for page in doc:
        texto += page.get_text()

    # --- CI ---
    ci_match = re.search(r"\d{7,8}-?\d", texto)
    ci = ci_match.group() if ci_match else None

    # --- Nombre ---
    nombre_match = re.search(r"Nombre.*?:\s*(.+)", texto)
    nombre = nombre_match.group(1).strip() if nombre_match else "No detectado"

    # --- HORARIOS (Formulario C) ---
    patron_horario = r"(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado)\s+(\d{1,2}:\d{2})\s*(?:a|-)\s*(\d{1,2}:\d{2})"

    horarios = []
    for match in re.findall(patron_horario, texto):
        horarios.append({
            "dia": match[0],
            "inicio": match[1],
            "fin": match[2]
        })

    # --- DECLARACIÓN ---
    declara_otros = False

    if re.search(r"no\s+declara\s+otros", texto, re.IGNORECASE):
        declara_otros = False
    elif re.search(r"declara\s+otros", texto, re.IGNORECASE):
        declara_otros = True

    return {
        "ci": ci,
        "nombre": nombre,
        "horarios": horarios,
        "declara_otros": declara_otros,
        "texto": texto
    }
