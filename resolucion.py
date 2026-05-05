from docx import Document

def generar_resolucion_word(data, output_path):

    doc = Document("resolucion_cfe.docx")

    texto = f"""
VISTO: acumulación de funciones de {data.get('nombre')} CI {data.get('ci')}

RESULTANDO:
Carga horaria: {data.get('horas_pdf')} horas

CONSIDERANDO:
{"Sin observaciones" if not data["observaciones"] else "Con observaciones"}

RESUELVE:

1) {"Autorizar" if not data["observaciones"] else "No autorizar"} acumulación
"""

    doc.add_paragraph(texto)
    doc.save(output_path)
