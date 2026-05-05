import fitz
import pytesseract
from PIL import Image
import re
import unicodedata


def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    texto = texto.replace("\n", " ")
    return texto


def ocr_pdf(doc):
    texto = ""

    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        texto += pytesseract.image_to_string(img, lang="spa")

    return texto


def extraer_datos_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")

    texto_directo = ""
    for page in doc:
        texto_directo += page.get_text()

    # decidir si usar OCR
    if len(texto_directo.strip()) < 100:
        texto = ocr_pdf(doc)
        fuente = "OCR"
    else:
        texto = texto_directo
        fuente = "PDF"

    texto_norm = normalizar(texto)

    # CI
    ci_match = re.search(r"\d{7,8}-?\d", texto_norm)
    ci = ci_match.group() if ci_match else None

    # Nombre
    nombre = "No detectado"
    m = re.search(r"nombre.*?:\s*([a-z\s]+)", texto_norm)
    if m:
        nombre = m.group(1).strip().title()

    # Horarios
    patron = r"(lunes|martes|miercoles|jueves|viernes|sabado)\s*(\d{1,2}[:.]?\d{0,2})\s*(a|-)\s*(\d{1,2}[:.]?\d{0,2})"

    horarios = []

    for match in re.findall(patron, texto_norm):

        def fix(h):
            if ":" not in h:
                return f"{h}:00"
            return h.replace(".", ":")

        horarios.append({
            "dia": match[0],
            "inicio": fix(match[1]),
            "fin": fix(match[3])
        })

    return {
        "ci": ci,
        "nombre": nombre,
        "horarios": horarios,
        "fuente": fuente,
        "texto": texto
    }
