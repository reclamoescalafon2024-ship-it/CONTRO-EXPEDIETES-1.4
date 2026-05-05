import fitz
import re
import unicodedata
import numpy as np
from PIL import Image

from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='es')


# -------------------------
# NORMALIZACIÓN
# -------------------------
def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    texto = texto.replace("\n", " ")
    return texto


# -------------------------
# TEXTO DIRECTO
# -------------------------
def extraer_texto_directo(doc):
    texto = ""
    for page in doc:
        texto += page.get_text()
    return texto


# -------------------------
# OCR
# -------------------------
def extraer_texto_ocr(doc):
    texto = ""

    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        result = ocr.ocr(np.array(img), cls=True)

        for line in result:
            for word in line:
                texto += word[1][0] + " "

    return texto


# -------------------------
# DECISIÓN INTELIGENTE
# -------------------------
def usar_ocr(texto):
    if len(texto.strip()) < 100:
        return True

    # si tiene muy pocos números/palabras útiles
    palabras = texto.split()
    if len(palabras) < 30:
        return True

    return False


# -------------------------
# EXTRACCIÓN PRINCIPAL
# -------------------------
def extraer_datos_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")

    texto_directo = extraer_texto_directo(doc)

    if usar_ocr(texto_directo):
        texto = extraer_texto_ocr(doc)
        fuente = "OCR"
    else:
        texto = texto_directo
        fuente = "PDF"

    texto_norm = normalizar(texto)

    # -------------------------
    # CI
    # -------------------------
    ci_match = re.search(r"\d{7,8}-?\d", texto_norm)
    ci = ci_match.group() if ci_match else None

    # -------------------------
    # NOMBRE
    # -------------------------
    nombre = "No detectado"

    patrones = [
        r"nombre.*?:\s*([a-z\s]+)",
        r"docente\s*:\s*([a-z\s]+)"
    ]

    for p in patrones:
        m = re.search(p, texto_norm)
        if m:
            nombre = m.group(1).strip().title()
            break

    # -------------------------
    # HORARIOS FLEXIBLES
    # -------------------------
    dias = "lunes|martes|miercoles|jueves|viernes|sabado"

    patron = rf"({dias})\s*(de)?\s*(\d{{1,2}}[:.]?\d{{0,2}})\s*(a|-)\s*(\d{{1,2}}[:.]?\d{{0,2}})"

    horarios = []

    for match in re.findall(patron, texto_norm):

        def fix(h):
            h = h.replace(".", ":")
            if ":" not in h:
                return f"{h}:00"
            return h

        horarios.append({
            "dia": match[0],
            "inicio": fix(match[2]),
            "fin": fix(match[4])
        })

    return {
        "ci": ci,
        "nombre": nombre,
        "horarios": horarios,
        "fuente": fuente,
        "texto": texto
    }
