import streamlit as st

from pdf_reader import extraer_datos_pdf
from validador import validar_datos
from informe import generar_informe

st.set_page_config(page_title="Contralor Digital PDF")

st.title("Contralor Digital - Solo Expediente")

# SOLO PDF
pdf = st.file_uploader("Subir expediente PDF", type="pdf")

if st.button("Analizar expediente"):

    if not pdf:
        st.error("Debe subir el expediente PDF")
        st.stop()

    # -------------------------
    # LECTURA
    # -------------------------
    data_pdf = extraer_datos_pdf(pdf)

    st.subheader("Datos detectados")
    st.write(data_pdf)

    # -------------------------
    # VALIDACIÓN
    # -------------------------
    resultado = validar_datos(data_pdf)

    st.subheader("Resultado de controles")
    st.write(resultado)

    # -------------------------
    # INFORME
    # -------------------------
    informe = generar_informe(resultado)

    st.subheader("Informe técnico")
    st.text(informe)

    st.download_button(
        "Descargar Informe",
        informe,
        file_name="informe.txt"
    )
