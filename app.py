import streamlit as st
import sqlite3
from PIL import Image
import time

def clear_text():
    st.session_state["matricula"] = ""
    st.session_state["apellido_1"] = ""
    st.session_state["apellido_2"] = ""

def main():

    con = sqlite3.connect("./data/lific.db")
    cur = con.cursor()

    logos = Image.open('./img/logos_UFRO.png')
    st.image(logos, width = 400)

    st.title('LIFIC - Línea Integradora de Formación en Ingeniería y Ciencias')

    matricula = st.text_input('Matrícula', key = 'matricula').upper()
    apellido_1 = st.text_input('Apellido 1', key = 'apellido_1').upper()
    apellido_2 = st.text_input('Apellido 2', key = 'apellido_2').upper()
    asignatura = st.selectbox("Asignatura", ['A1', 'A2', 'A3', 'Histórico']).lower()
    
    clicked = st.button('Buscar')
    reset = st.button('Limpiar', on_click = clear_text)
    
    if asignatura == 'histórico':
        query = f"SELECT estudiantes.matricula, nombres, apellido_1, apellido_2, estudiantes.carrera, estudiantes.sexo, a1.asignatura, a1.año, a1.semestre, a1.promedio_final, a1.estado,a2.asignatura, a2.año, a2.semestre, a2.promedio_final, a2.estado,a3.asignatura, a3.año, a3.semestre, a3.promedio_final, a3.estado  FROM estudiantes LEFT JOIN a1 on estudiantes.matricula = a1.matricula LEFT JOIN a2 on estudiantes.matricula = a2.matricula LEFT JOIN a3 on estudiantes.matricula = a3.matricula WHERE (apellido_1 = '{apellido_1}' AND apellido_2 = '{apellido_2}') or estudiantes.matricula = '{matricula}'"
    else:
        query = f"SELECT estudiantes.matricula, nombres, apellido_1, apellido_2, estudiantes.carrera, estudiantes.sexo, {asignatura}.asignatura, año, semestre, promedio_final, estado FROM estudiantes INNER JOIN {asignatura} ON estudiantes.matricula = {asignatura}.matricula WHERE (apellido_1 = '{apellido_1}' AND apellido_2 = '{apellido_2}') OR estudiantes.matricula = '{matricula}'"

    if clicked:
        with st.spinner("Obteniendo información..."):
            time.sleep(0.2)
        res = cur.execute(query).fetchall()
        st.text(res)
        if res != []:
            col1, col2 = st.columns(2)
            with col1:
                if res[0][5] == 'Femenino':
                    icon = Image.open('./img/icon_woman.png')
                else:
                    icon = Image.open('./img/icon_man.png')
                st.image(icon, width = 250)
            
            with col2:
                st.header(res[0][1] + ' ' + res[0][2] + ' ' + res[0][3])
                st.header(res[0][0])
                st.header(res[0][4])
            st.dataframe(data = res)
        else:
            st.text("No se registra información.")
    
    

    if reset:
        clicked = False
    

if __name__ == "__main__":
    main()