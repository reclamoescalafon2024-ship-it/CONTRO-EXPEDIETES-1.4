import streamlit as st
import pandas as pd

from pdf_reader import extraer_datos_pdf
from validador import validar_datos
from informe import generar_informe
from resolucion_word import generar_resolucion_word

st.set_page_config(page_title="Contralor Digital")

st.title("Contralor Digital - OK")

pdf = st.file_uploader("Expediente PDF", type="pdf")
excel_horas = st.file_uploader("Excel Horas", type="xlsx")
excel_dsf = st.file_uploader("Excel DSF", type="xlsx")

if st.button("Analizar"):

    if not pdf:
        st.error("Subí el PDF")
        st.stop()

    if not (excel_horas and excel_dsf):
        st.error("Subí ambos Excel")
        st.stop()

    data_pdf = extraer_datos_pdf(pdf)

    df_horas = pd.read_excel(excel_horas)
    df_dsf = pd.read_excel(excel_dsf)

    resultado = validar_datos(data_pdf, df_horas, df_dsf)

    st.write(resultado)

    informe = generar_informe(resultado)

    generar_resolucion_word(resultado, "resolucion.docx")

    st.download_button("Descargar Informe", informe, "informe.txt")

    with open("resolucion.docx", "rb") as f:
        st.download_button("Descargar Resolución", f, "resolucion.docx")
