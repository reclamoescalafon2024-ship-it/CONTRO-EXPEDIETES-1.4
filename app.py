import streamlit as st

from pdf_reader import extraer_datos_pdf
from validador import validar_datos
from informe import generar_informe

# ---------------------------------
# CONFIGURACIÓN
# ---------------------------------
st.set_page_config(page_title="Contralor Digital PDF", layout="wide")

st.title("📄 Contralor Digital de Expedientes")
st.write("Análisis automático desde PDF (con soporte OCR)")

# ---------------------------------
# SUBIDA DE ARCHIVO
# ---------------------------------
pdf = st.file_uploader("Subir expediente en PDF", type="pdf")

# ---------------------------------
# BOTÓN PRINCIPAL
# ---------------------------------
if st.button("Analizar expediente"):

    if not pdf:
        st.error("Debe subir un expediente en PDF")
        st.stop()

    # ---------------------------------
    # LECTURA DEL PDF
    # ---------------------------------
    with st.spinner("Procesando expediente..."):
        data = extraer_datos_pdf(pdf)

    # ---------------------------------
    # DEBUG / CONTROL
    # ---------------------------------
    st.subheader("🔍 Fuente de datos")
    st.write(data.get("fuente", "No especificado"))

    st.subheader("🧾 Texto detectado (preview)")
    st.text(data.get("texto", "")[:1500])

    # ---------------------------------
    # DATOS EXTRAÍDOS
    # ---------------------------------
    st.subheader("📌 Datos detectados")
    st.write({
        "CI": data.get("ci"),
        "Nombre": data.get("nombre"),
        "Horarios": data.get("horarios")
    })

    # ---------------------------------
    # VALIDACIÓN
    # ---------------------------------
    resultado = validar_datos(data)

    st.subheader("⚖️ Resultado del control")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Horas", resultado.get("total_horas", 0))
    col2.metric("Organismos", ", ".join(resultado.get("organismos", [])))
    col3.metric("Multiempleo", "Sí" if resultado.get("multiempleo") else "No")

    # ---------------------------------
    # SUPERPOSICIONES
    # ---------------------------------
    if resultado.get("conflictos"):
        st.error("❌ Se detectaron superposiciones horarias")
        st.write(resultado["conflictos"])
    else:
        st.success("✔ Sin superposición horaria")

    # ---------------------------------
    # OBSERVACIONES
    # ---------------------------------
    st.subheader("📝 Observaciones")

    if resultado.get("observaciones"):
        for o in resultado["observaciones"]:
            st.warning(o)
    else:
        st.success("Sin observaciones")

    # ---------------------------------
    # INFORME
    # ---------------------------------
    informe = generar_informe(resultado)

    st.subheader("📄 Informe técnico")
    st.text(informe)

    # ---------------------------------
    # DESCARGA
    # ---------------------------------
    st.download_button(
        label="⬇ Descargar informe",
        data=informe,
        file_name="informe_tecnico.txt",
        mime="text/plain"
    )
