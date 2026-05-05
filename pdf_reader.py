import fitz
import re
import unicodedata


def normalizar(texto):
    # Quita acentos y unifica formato
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

    # -----------------------------
    # CI (más flexible)
    # -----------------------------
    ci_match = re.search(r"\b\d{7,8}\s*-?\s*\d\b", texto)
    ci = ci_match.group().replace(" ", "") if ci_match else None

    # -----------------------------
    # NOMBRE (varias formas)
    # -----------------------------
    nombre = "No detectado"

    patrones_nombre = [
        r"nombre\s*(del|de)?\s*(docente|titular)?\s*:\s*([a-z\s]+)",
        r"docente\s*:\s*([a-z\s]+)",
    ]

    for p in patrones_nombre:
        m = re.search(p, texto)
        if m:
            nombre = m.group(m.lastindex).strip().title()
            break

    # -----------------------------
    # HORARIOS (MUY flexible)
    # -----------------------------
    dias = "lunes|martes|miercoles|jueves|viernes|sabado"

    patron_horario = rf"({dias})\s*(de)?\s*(\d{{1,2}}[:.]?\d{{0,2}})\s*(a|-)\s*(\d{{1,2}}[:.]?\d{{0,2}})"

    horarios = []

    for match in re.findall(patron_horario, texto):
        dia = match[0]

        def limpiar_hora(h):
            if ":" not in h:
                return f"{h}:00"
            return h.replace(".", ":")

        inicio = limpiar_hora(match[2])
        fin = limpiar_hora(match[4])

        horarios.append({
            "dia": dia.capitalize(),
            "inicio": inicio,
            "fin": fin
        })

    # -----------------------------
    # DECLARACIÓN (inteligente)
    # -----------------------------
    declara_otros = None

    if re.search(r"no\s+declara.*otros", texto):
        declara_otros = False

    elif re.search(r"declara.*otros", texto):
        declara_otros = True

    # fallback más amplio
    elif "otros vinculos" in texto:
        declara_otros = True

    # -----------------------------
    return {
        "ci": ci,
        "nombre": nombre,
        "horarios": horarios,
        "declara_otros": declara_otros,
        "texto": texto_raw  # dejamos original por si querés debug
    }
