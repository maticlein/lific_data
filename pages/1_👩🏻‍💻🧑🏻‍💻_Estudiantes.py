import streamlit as st
from PIL import Image
import sqlite3
import time
import pandas as pd

favicon = Image.open('./img/logo_innovacion.png')
st.set_page_config(
    page_title = "LIFIC Data - Estudiantes",
    page_icon = favicon 
)

def clear_text():
    st.session_state["matricula"] = ""
    st.session_state["apellido_1"] = ""
    st.session_state["apellido_2"] = ""

logos = Image.open('./img/logos_UFRO.png')
st.image(logos, width = 400)
st.title('LIFIC - Línea Integradora de Formación en Ingeniería y Ciencias')

con = sqlite3.connect("./data/lific.db")
cur = con.cursor()

matricula = st.text_input('Matrícula', key = 'matricula').upper().strip()
apellido_1 = st.text_input('Apellido 1', key = 'apellido_1').upper().strip()
apellido_2 = st.text_input('Apellido 2', key = 'apellido_2').upper().strip()
asignatura = st.selectbox("Asignatura", ['A1', 'A2', 'A3', 'Histórico']).lower()

clicked = st.button('Buscar')
reset = st.button('Limpiar', on_click = clear_text)
    
if asignatura == 'histórico':
    query = f"SELECT estudiantes.matricula, nombres, apellido_1, apellido_2, estudiantes.carrera, estudiantes.sexo, a1.año, a1.semestre, a1.promedio_final, a1.estado, a2.año, a2.semestre, a2.promedio_final, a2.estado, a3.año, a3.semestre, a3.promedio_final, a3.estado  FROM estudiantes LEFT JOIN a1 on estudiantes.matricula = a1.matricula LEFT JOIN a2 on estudiantes.matricula = a2.matricula LEFT JOIN a3 on estudiantes.matricula = a3.matricula WHERE (apellido_1 = '{apellido_1}' AND apellido_2 = '{apellido_2}') or estudiantes.matricula = '{matricula}'"
    columns = ['matricula', 'nombres', 'apellido_1', 'apellido_2', 'carrera', 'sexo', 'año_a1', 'semestre_a1', 'promedio_final_a1', 'estado_a1', 'año_a2', 'semestre_a2', 'promedio_final_a2', 'estado_a2', 'año_a3', 'semestre_a3', 'promedio_final_a3', 'estado_a3']
else:
    query = f"SELECT estudiantes.matricula, nombres, apellido_1, apellido_2, estudiantes.carrera, estudiantes.sexo, {asignatura}.asignatura, año, semestre, promedio_final, estado FROM estudiantes INNER JOIN {asignatura} ON estudiantes.matricula = {asignatura}.matricula WHERE (apellido_1 = '{apellido_1}' AND apellido_2 = '{apellido_2}') OR estudiantes.matricula = '{matricula}'"
    columns = ['matricula', 'nombres', 'apellido_1', 'apellido_2', 'carrera', 'sexo', 'asignatura', 'año', 'semestre', 'promedio_final', 'estado']
if clicked:
    with st.spinner("Obteniendo información..."):
        time.sleep(0.2)
    res = cur.execute(query).fetchall()
    if res != []:
        for estudiante in res:
            col1, col2 = st.columns(2)
            with col1:
                if estudiante[5] == 'Femenino':
                    icon = Image.open('./img/icon_woman.png')
                else:
                    icon = Image.open('./img/icon_man.png')
                st.image(icon, width = 250)           
            with col2:
                st.header(estudiante[1] + ' ' + estudiante[2] + ' ' + estudiante[3])
                st.header(estudiante[0])
                st.header(estudiante[4])
        data = pd.DataFrame(res, columns = columns)
        st.dataframe(data = data)
    else:
        st.text("No se registra información.")
    
if reset:
    clicked = False