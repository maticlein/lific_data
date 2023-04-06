import streamlit as st
from PIL import Image
import sqlite3
import pandas as pd
import plotly.graph_objects as go

favicon = Image.open('./img/logo_innovacion.png')
st.set_page_config(
    page_title = "LIFIC Data - Estadísticas",
    page_icon = favicon 
)

logos = Image.open('./img/logos_UFRO.png')
st.image(logos, width = 400)
st.title('LIFIC - Línea Integradora de Formación en Ingeniería y Ciencias')

con = sqlite3.connect("./data/lific.db")
cur = con.cursor()

st.markdown('***')

st.header('Estado de estudiantes por cohorte')
query = "SELECT estado_estudiante, COUNT(*) as total_estudiantes from estudiantes WHERE SUBSTRING(matricula, -2, 2) = '22' GROUP BY estado_estudiante order BY total_estudiantes DESC"
fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = ["Cohorte 2022", "Activos", "Postergación de estudios", "Retiro temporal", "Eliminación por reglamento", "Renuncia a la carrera", "Abandono de estudios", "Inactivo", "Renuncia voluntaria", "Cambio de carrera", "Cohorte 2021", "Inactivo", "Cohorte 2020", "Cohorte 2019", "Cohorte 2018", "Cohorte 2017", "Cohorte 2023"],
      color = "blue"
    ),
    link = dict(
      source = [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 12, 12, 13, 14, 14, 15, 16],
      target = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 11, 4, 8, 5, 1, 8, 1, 1, 9, 1, 1],
      value = [371, 28, 15, 15, 13, 13, 11, 6, 6, 72, 2, 2, 1, 1, 24, 1, 12, 4, 1, 1, 535], 
      color = ["rgba(31, 119, 180, 0.8)",
               "rgba(255, 127, 14, 0.8)",
               "rgba(44, 160, 44, 0.8)",
               "rgba(214, 39, 40, 0.8)",
               "rgba(148, 103, 189, 0.8)",
               "rgba(140, 86, 75, 0.8)",
               "rgba(227, 119, 194, 0.8)",
               "rgba(127, 127, 127, 0.8)",
               "rgba(188, 189, 34, 0.8)",
               "rgba(31, 119, 180, 0.8)",
               "rgba(18, 109, 100, 0.8)",
               "rgba(214, 39, 40, 0.8)",
               "rgba(127, 127, 127, 0.8)",
               "rgba(148, 103, 189, 0.8)",
               "rgba(31, 119, 180, 0.8)",
               "rgba(127, 127, 127, 0.8)",
               "rgba(31, 119, 180, 0.8)",
               "rgba(31, 119, 180, 0.8)",
               "rgba(188, 189, 34, 0.8)",
               "rgba(31, 119, 180, 0.8)",
               "rgba(31, 119, 180, 0.8)",
               ]
  ))])

st.plotly_chart(fig.update_layout(font_size = 20))

st.markdown('***')

st.header('Desglose de Estudiantes')

col1, col2, col3 = st.columns(3)

with col1:
    st.caption('Estados')
    query = "SELECT estado_estudiante, COUNT(*) as estudiantes_totales FROM estudiantes GROUP BY estado_estudiante ORDER BY estudiantes_totales DESC"
    res = cur.execute(query).fetchall()
    data = pd.DataFrame(res, columns = ['Carrera', 'Cantidad'])
    st.dataframe(data = data)

with col2:
    st.caption('Activos por carrera')
    query = "SELECT carrera, COUNT(*) as estudiantes_totales FROM estudiantes WHERE estado_estudiante = 'Activo' GROUP BY carrera ORDER BY estudiantes_totales DESC"
    res = cur.execute(query).fetchall()
    data = pd.DataFrame(res, columns = ['Carrera', 'Cantidad'])
    st.dataframe(data = data)

with col3:
    st.caption('Activos por sexo')
    query = "SELECT sexo, COUNT(*) as estudiantes_totales FROM estudiantes WHERE estado_estudiante = 'Activo' GROUP BY sexo ORDER BY estudiantes_totales DESC"
    res = cur.execute(query).fetchall()
    data = pd.DataFrame(res, columns = ['Sexo', 'Cantidad'])
    data.replace(['M', 'F'], ["Masculino", "Femenino"], inplace = True)
    st.dataframe(data = data)

st.markdown('***')