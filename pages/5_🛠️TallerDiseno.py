import streamlit as st
from PIL import Image
import pandas as pd
import time
import modules.competences as cmpt 

favicon = Image.open('./img/logo_innovacion.png')
st.set_page_config(
    page_title = "LIFIC Data - Docentes",
    page_icon = favicon 
)

logos = Image.open('./img/logos_UFRO.png')
st.image(logos, width = 400)
st.title('LIFIC - Línea Integradora de Formación en Ingeniería y Ciencias')
st.header('ING200 - Taller de Diseño de Ingeniería')
st.markdown("***")

st.header('Competencias, Resultados de Aprendizaje, Categorías e Indicadores de Logro')
st.plotly_chart(cmpt.competences_sunburst_plot(), use_container_width=True)
cmpt.competences_info()

st.markdown("***")
st.header("Evaluación de Anteproyecto")
rubrica = st.file_uploader(label = "Sube la rúbrica de anteproyecto ", type = ['xlsx'], accept_multiple_files = False,)
if rubrica is not None:
    df_rubrica = pd.read_excel(rubrica, header = 1).drop("Unnamed: 11", axis = 1).drop([15, 16, 17], axis = 0)
    df_problematica = df_rubrica[df_rubrica["Categorías Evaluadas de las Competencias"] == "Problemática"]
    df_propuesta_solucion = df_rubrica[df_rubrica["Categorías Evaluadas de las Competencias"] == "Propuesta de la Solución"]
    df_documentacion = df_rubrica[df_rubrica["Categorías Evaluadas de las Competencias"] == "Documentación"]    
    options = [column for column in df_problematica.columns if "Grupo" in str(column)]    
    option = st.selectbox('Grupos', options)
    if option is not None:
        problematica = 0
        propuesta_solucion = 0
        documentacion = 0
        for index, row in df_problematica.iterrows():
            problematica += row["Porcentaje"] * 100 * (row[option] / 3)
        for index, row in df_propuesta_solucion.iterrows():
            propuesta_solucion += row["Porcentaje"] * 100 * (row[option] / 3)
        for index, row in df_documentacion.iterrows():
            documentacion += row["Porcentaje"] * 100 * (row[option] / 3)
        problematica = round(problematica, 1)
        propuesta_solucion = round(propuesta_solucion, 1)
        documentacion = round(documentacion, 1)
        st.write(f"Problemática: {problematica}% de 25%")
        st.plotly_chart(cmpt.progress_plot(problematica, "Problemática"), use_container_width=True)
        st.write(f"Propuesta de la Solución: {propuesta_solucion}% de 60%")
        st.plotly_chart(cmpt.progress_plot(propuesta_solucion, "Propuesta de la Solución"), use_container_width=True)
        st.write(f"Documentación: {documentacion}% de 15%")
        st.plotly_chart(cmpt.progress_plot(documentacion, "Documentación"), use_container_width=True)



st.markdown("***")
st.header('Reporte de resultados')
uploaded_file = st.file_uploader(label = "Sube el archivo de notas", type = ['csv'], accept_multiple_files = False,)
if uploaded_file is not None: 
    data = pd.read_csv(uploaded_file, sep = ";")
    option = st.selectbox(label = 'Grupo', options = [f"Grupo {x}" for x in data['grupo']])
    group = int(option.split()[1])
    datos = data[data["grupo"] == group]
    design = list(datos['diseno'])[0]
    innovation = list(datos['innovacion'])[0]
    social_resp = list(datos['resp_social'])[0]
    st.title(option)
    st.plotly_chart(cmpt.progress_plot(design, "Diseño"), use_container_width=True)
    st.markdown(f"- {design}%: {cmpt.competence_result(design, 'Diseño')}")
    st.plotly_chart(cmpt.progress_plot(innovation, "Innovación"), use_container_width=True)
    st.markdown(f"- {innovation}%: {cmpt.competence_result(innovation, 'Innovación')}")
    st.plotly_chart(cmpt.progress_plot(social_resp, "Responsabilidad Social"), use_container_width=True)
    st.markdown(f"- {social_resp}%: {cmpt.competence_result(social_resp, 'Responsabilidad Social')}")
    if st.button(label='Generar Reporte'):
        with st.spinner('Generando...'):
            time.sleep(5)
        cmpt.generate_report(option, group, design, innovation, social_resp)

    st.markdown("***")
    st.header('Comparación Competencias Desarrolladas')
    options = st.multiselect('Grupos',
                            [f"Grupo {x}" for x in range (1, 7)],
                            [option])
    st.plotly_chart(cmpt.group_comparison(data, options), use_container_width = True)
    st.write("***")