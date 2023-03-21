import streamlit as st
import sqlite3

def clear_text():
    st.session_state["matricula"] = ""
    st.session_state["apellido_1"] = ""
    st.session_state["apellido_2"] = ""

def main():

    con = sqlite3.connect("./data/lific.db")
    cur = con.cursor()

    matricula = st.text_input('Matrícula', key = 'matricula').upper()
    apellido_1 = st.text_input('Apellido 1', key = 'apellido_1').upper()
    apellido_2 = st.text_input('Apellido 2', key = 'apellido_2').upper()
    asignatura = st.selectbox("Asignatura", ['A1', 'A2', 'A3', 'Histórico']).lower()
    
    clicked = st.button('Buscar')
    reset = st.button('Limpiar', on_click = clear_text)
    
    if asignatura == 'histórico':
        query = f"SELECT estudiantes.matricula, nombres, apellido_1, apellido_2, a1.asignatura, a1.año, a1.semestre, a1.promedio_final, a1.estado,a2.asignatura, a2.año, a2.semestre, a2.promedio_final, a2.estado,a3.asignatura, a3.año, a3.semestre, a3.promedio_final, a3.estado  FROM estudiantes LEFT JOIN a1 on estudiantes.matricula = a1.matricula LEFT JOIN a2 on estudiantes.matricula = a2.matricula LEFT JOIN a3 on estudiantes.matricula = a3.matricula WHERE (apellido_1 = '{apellido_1}' AND apellido_2 = '{apellido_2}') or estudiantes.matricula = '{matricula}'"
    else:
        query = f"SELECT nombres, apellido_1, apellido_2, {asignatura}.asignatura, año, semestre, promedio_final, estado FROM estudiantes INNER JOIN {asignatura} ON estudiantes.matricula = {asignatura}.matricula WHERE (apellido_1 = '{apellido_1}' AND apellido_2 = '{apellido_2}') OR estudiantes.matricula = '{matricula}'"

    if clicked:
        res = cur.execute(query).fetchall()
        if res != []:
            st.dataframe(data = res)
        else:
            st.text("No se registra información.")
    
    if reset:
        clicked = False
    

if __name__ == "__main__":
    main()