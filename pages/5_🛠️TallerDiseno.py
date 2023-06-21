import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import pandas as pd

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

st.header('Competencias desarrolladas')

diseno = st.slider("Diseño", min_value = 1, max_value = 7, step = 1, label_visibility = 'visible')
innovacion = st.slider("Innovación", min_value = 1, max_value = 7, step = 1, label_visibility = 'visible')
resp_social = st.slider("Responsabilidad Social", min_value = 1, max_value = 7, step = 1, label_visibility = 'visible')

df = pd.DataFrame(dict(
    valor = [diseno, innovacion, resp_social],
    competencia = ['Diseño','Innovación','Responsabilidad Social']))

fig = go.Figure()


fig.add_trace(go.Scatterpolar(
      r = [7, 7, 7],
      theta = df["competencia"],
      fill = 'toself',
      name = 'Esperado',
))

fig.add_trace(go.Scatterpolar(
      r = df["valor"],
      theta=df["competencia"],
      fill='toself',
      name='Estudiante',
      fillcolor = "#C03278",
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[1, 7]
    )),
  showlegend=False
)

st.plotly_chart(fig, use_container_width = True)