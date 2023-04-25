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

option = st.selectbox("Modalidad de búsqueda", ("Asignatura", "Histórico"))

matricula = st.text_input('Matrícula', key = 'matricula').upper().strip()
st.text("O")
apellido_1 = st.text_input('Apellido 1', key = 'apellido_1').upper().strip()
apellido_2 = st.text_input('Apellido 2', key = 'apellido_2').upper().strip()
if option == 'Asignatura':
    asignatura = st.selectbox("Asignatura", ['A1', 'A2', 'A3', 'A4']).lower()

clicked = st.button('Buscar')
reset = st.button('Limpiar', on_click = clear_text)

st.markdown("***")

if option == 'Asignatura':
    query = f"SELECT estudiantes.matricula, nombres, apellido_1, apellido_2, carrera, sexo, estado_estudiante, {asignatura}.asignatura, año, semestre, promedio_final, estado_asignatura FROM estudiantes INNER JOIN {asignatura} ON estudiantes.matricula = {asignatura}.matricula WHERE (apellido_1 = '{apellido_1}' AND apellido_2 = '{apellido_2}') OR estudiantes.matricula = '{matricula}'"
    columns = ['matricula', 'nombres', 'apellido_1', 'apellido_2', 'carrera', 'sexo', 'asignatura', 'año', 'semestre', 'promedio_final', 'estado']
else:
    query = f"SELECT estudiantes.matricula, nombres, apellido_1, apellido_2, carrera, sexo, estado_estudiante, a1.año, a1.semestre, a1.promedio_final AS promedio_A1, a1.estado_asignatura AS estado_A1, a2.año, a2.semestre, a2.promedio_final AS promedio_A2, a2.estado_asignatura AS estado_A2, a3.año, a3.semestre, a3.promedio_final AS promedio_A3, a3.estado_asignatura AS estado_A3, a4.año, a4.semestre, a4.promedio_final AS promedio_A4, a4.estado_asignatura AS estado_A4 FROM estudiantes LEFT JOIN a1 ON estudiantes.matricula = a1.matricula LEFT JOIN a2 ON estudiantes.matricula = a2.matricula LEFT JOIN a3 ON estudiantes.matricula = a3.matricula LEFT JOIN a4 ON estudiantes.matricula = a4.matricula WHERE estudiantes.matricula = '{matricula}' or (apellido_1 = '{apellido_1}' AND apellido_2 = '{apellido_2}') order by a1.año desc, a1.semestre desc, a2.año desc, a2.semestre desc, a3.año desc, a3.semestre desc, a4.año desc, a4.semestre desc LIMIT 1"
    columns = ['matricula', 'nombres', 'apellido_1', 'apellido_2', 'carrera', 'sexo', 'año_a1', 'semestre_a1', 'promedio_final_a1', 'estado_a1', 'año_a2', 'semestre_a2', 'promedio_final_a2', 'estado_a2', 'año_a3', 'semestre_a3', 'promedio_final_a3', 'estado_a3', 'año_a4', 'semestre_a4', 'promedio_final_a4', 'estado_a4']
if clicked:
    with st.spinner("Obteniendo información..."):
        time.sleep(0.2)
    res = cur.execute(query).fetchall()
    if res != []:
        for estudiante in res:
            col1, col2 = st.columns(2)
            with col1:
                if estudiante[5] == 'F':
                    icon = Image.open('./img/icon_woman.png')
                else:
                    icon = Image.open('./img/icon_man.png')
                st.image(icon, width = 250)           
            with col2:
                st.header(estudiante[1] + ' ' + estudiante[2] + ' ' + estudiante[3])
                st.header(estudiante[0])
                st.header(estudiante[4])  
                st.header(estudiante[6])  
        col1, col2, col3, col4, col5 = st.columns(5)
        if option == 'Asignatura':
            data = pd.DataFrame({'Año': [res[0][8]], 'Semestre': [res[0][9]], 'Promedio': [res[0][10]], 'Estado': [res[0][11]]}, index = [res[0][7]])
            st.table(data)
        else:
            data = pd.DataFrame({'Año': [res[0][7], res[0][11], res[0][15], res[0][19]], 'Semestre': [res[0][8], res[0][12], res[0][16], res[0][20]], 'Promedio': [res[0][9], res[0][13], res[0][17], res[0][21]], 'Estado': [res[0][10], res[0][14], res[0][18], res[0][22]]}, dtype = 'int', index = ['A1', 'A2', 'A3', 'A4'])
            data.fillna(value = '-', inplace = True)
            data = data.replace('', '-')
            st.table(data)
    else:
        st.text("No se registra información.")
        
if reset:
    clicked = False

st.markdown("***")