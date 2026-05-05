import fitz
import re
import unicodedata

DIAS = ["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]

def normalizar(t):
    t = t.lower()
    t = unicodedata.normalize('NFKD', t).encode('ascii','ignore').decode()
    t = t.replace("\n"," ")
    t = re.sub(r"\s+", " ", t)
    return t

def norm_hora(h):
    h = h.replace(".", ":")
    if ":" not in h:
        return f"{int(h):02d}:00"
    hh, mm = h.split(":")
    mm = mm if mm else "00"
    return f"{int(hh):02d}:{int(mm):02d}"

def detectar_organismo(fragmento):
    if "cfe" in fragmento:
        return "CFE"
    if "secundaria" in fragmento or "dges" in fragmento:
        return "DGES"
    if "utec" in fragmento:
        return "UTEC"
    return "OTRO"

def extraer_datos_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")

    raw = ""
    for p in doc:
        raw += p.get_text()

    txt = normalizar(raw)

    # --- CI
    m = re.search(r"\b\d{7,8}\s*-?\s*\d\b", txt)
    ci = m.group().replace(" ", "") if m else None

    # --- Nombre
    nombre = "No detectado"
    pats = [
        r"nombre\s*(del|de)?\s*(docente|titular)?\s*:\s*([a-z\s]+)",
        r"docente\s*:\s*([a-z\s]+)"
    ]
    for p in pats:
        m = re.search(p, txt)
        if m:
            nombre = m.group(m.lastindex).strip().title()
            break

    # --- HORARIOS (flexible)
    # Ej: lunes 8 a 10 | lunes 08:00-10:30 | lunes de 8.30 a 11
    dias = "|".join(DIAS)
    patron = rf"({dias})\s*(de)?\s*(\d{{1,2}}[:.]?\d{{0,2}})\s*(a|-|–)\s*(\d{{1,2}}[:.]?\d{{0,2}})"

    horarios = []
    for m in re.finditer(patron, txt):
        dia = m.group(1)
        h1 = norm_hora(m.group(3))
        h2 = norm_hora(m.group(5))

        # Tomamos una ventana de texto alrededor para inferir organismo
        start = max(0, m.start()-80)
        end = min(len(txt), m.end()+80)
        frag = txt[start:end]
        org = detectar_organismo(frag)

        horarios.append({
            "dia": dia.capitalize(),
            "inicio": h1,
            "fin": h2,
            "organismo": org
        })

    # --- Declaración (simple)
    declara_otros = None
    if re.search(r"no\s+declara.*otros", txt):
        declara_otros = False
    elif re.search(r"declara.*otros", txt):
        declara_otros = True

    return {
        "ci": ci,
        "nombre": nombre,
        "horarios": horarios,
        "declara_otros": declara_otros,
        "texto": raw
    }
