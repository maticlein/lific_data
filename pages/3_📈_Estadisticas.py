import streamlit as st
from PIL import Image
import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px
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

st.header('Resultados asignatura')

asignatura = st.selectbox("Seleccione asignatura", ('A1', 'A2', 'A3', 'A4')).lower()
anio = st.selectbox("Seleccione año", ('2022', '2023'))
semestre = st.selectbox("Seleccione semestre", (1, 2))

query = f"SELECT estudiantes.matricula, nombres, apellido_1, apellido_2, carrera, sexo, estado_estudiante, taller_1, taller_2, taller_3, promedio_final, estado_asignatura FROM estudiantes INNER JOIN {asignatura} ON estudiantes.matricula = {asignatura}.matricula WHERE año = {anio} AND semestre = {semestre} AND estado_asignatura != 'Convalidada'"

res = cur.execute(query).fetchall()
data = pd.DataFrame(data = res, columns = ['matricula', 'nombres', 'apellido_1', 'apellido_2', 'carrera', 'sexo', 'estado_estudiante', 'taller_1', 'taller_2', 'taller_3', 'promedio_final', 'estado_asignatura'], dtype = 'float')

col1, col2, col3, col4 = st.columns(4)
with col1:
    inscritos = data
    st.metric('Estudiantes Inscritos', len(inscritos))
with col2:
    activos = data[(data['estado_asignatura'] == 'Aprobada') | (data['estado_asignatura'] == 'Reprobada')]
    st.metric('Estudiantes Activos', len(activos))
with col3:
    aprobados = data[data['estado_asignatura'] == 'Aprobada']
    st.metric('Estudiantes Aprobados', len(aprobados))
with col4:
    aprobados = data[data['estado_asignatura'] == 'Reprobada']
    st.metric('Estudiantes Reprobados', len(aprobados)) 

col1, col2, col3, col4 = st.columns(4)
with col1:
    inscritos = data[(data['estado_asignatura'] == 'Aprobada') | (data['estado_asignatura'] == 'Reprobada')]
    st.metric('Promedio Inscritos', round(inscritos['promedio_final'].astype('float').mean(), 1)) 

with col2:
    aprobados = data[data['estado_asignatura'] == 'Aprobada']
    st.metric('Promedio Aprobados', round(aprobados['promedio_final'].astype('float').mean(), 1))

with col3:
    mujeres = data[(data['sexo'] == 'F') & ((data['estado_asignatura'] == 'Aprobada') | (data['estado_asignatura'] == 'Reprobada'))]
    st.metric('Promedio Mujeres', round(mujeres['promedio_final'].astype('float').mean(), 1))

with col4:
    hombres = data[(data['sexo'] == 'M') & ((data['estado_asignatura'] == 'Aprobada') | (data['estado_asignatura'] == 'Reprobada'))]
    st.metric('Promedio Hombres', round(hombres['promedio_final'].astype('float').mean(), 1))

talleres_activos = data[(data['estado_asignatura'] == 'Aprobada') | (data['estado_asignatura'] == 'Reprobada')]
talleres_aprobados = data[(data['estado_asignatura'] == 'Aprobada')]
prom_taller1 = round(talleres_activos['taller_1'].replace("#N/D", np.nan).dropna().astype('float').mean(), 1)
prom_taller2 = round(talleres_activos['taller_2'].replace("#N/D", np.nan).dropna().astype('float').mean(), 1)
prom_taller3 = round(talleres_activos['taller_3'].replace("#N/D", np.nan).dropna().astype('float').mean(), 1)
prom_taller1_ap = round(talleres_aprobados['taller_1'].replace("#N/D", np.nan).dropna().astype('float').mean(), 1)
prom_taller2_ap = round(talleres_aprobados['taller_2'].replace("#N/D", np.nan).dropna().astype('float').mean(), 1)
prom_taller3_ap = round(talleres_aprobados['taller_3'].replace("#N/D", np.nan).dropna().astype('float').mean(), 1)
notas = pd.DataFrame(
    {'tipo': ['taller_1', 'taller_2', 'taller_3', 'taller_1', 'taller_2', 'taller_3'],
     'estudiantes': ['inscritos', 'inscritos', 'inscritos', 'aprobados', 'aprobados', 'aprobados'],
     'nota': [prom_taller1, prom_taller2, prom_taller3, prom_taller1_ap, prom_taller2_ap, prom_taller3_ap]}
)
fig = px.histogram(notas, x="tipo", y="nota", color = 'estudiantes', barmode='group', range_y=[1, 7])
st.plotly_chart(fig)

fig = px.pie(data['sexo'], names = 'sexo', title = 'Distribución por sexo')
fig.update_layout(font = {"size": 18})
st.plotly_chart(fig)

fig = px.pie(data['estado_asignatura'], names = 'estado_asignatura', title = 'Distribución por estado')
fig.update_layout(font = {"size": 18})
st.plotly_chart(fig)

st.dataframe(data)
st.markdown('***')