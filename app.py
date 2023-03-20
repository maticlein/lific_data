import streamlit as st
import sqlite3

def main():

    con = sqlite3.connect("./data/lific.db")
    cur = con.cursor()

    apellido_1 = st.text_input('Apellido 1').upper()
    apellido_2 = st.text_input('Apellido 2').upper()

    st.title(f"{apellido_1} {apellido_2}")
    
    res = cur.execute(f"SELECT nombres, apellido_1, apellido_2, a1.asignatura, año, semestre, promedio_final, estado FROM estudiantes INNER JOIN a1 ON estudiantes.matricula = a1.matricula WHERE apellido_1 = '{apellido_1}' AND apellido_2 = '{apellido_2}'").fetchall()

    st.dataframe(data = res)
if __name__ == "__main__":
    main()