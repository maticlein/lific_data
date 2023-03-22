import streamlit as st
from PIL import Image
import sqlite3
import pandas as pd

favicon = Image.open('./img/logo_innovacion.png')
st.set_page_config(
    page_title = "LIFIC Data - DB",
    page_icon = favicon 
)

def clear_text():
    st.session_state["query"] = ""

st.title('Campos tablas DB')

with st.expander('docentes'):
    st.markdown("- docente_id\n- nombres\n- apellido_1\n- apellido_2\n- sexo\n- titulo\n- mail")

with st.expander('estudiantes'):
    st.markdown("- matricula\n- nombres\n- apellido_1\n- apellido_2\n- mail\n- carrera\n- sexo")

with st.expander('aX'):
    st.markdown("- aX_id\n- asignatura\n- matricula\n- año\n- semestre\n- modulo\n- docente\n- notas\n- asistencia\n- promedio_final\n- estado")


st.title('DB Playground')

con = sqlite3.connect("./data/lific.db")
cur = con.cursor()

query = st.text_area('Query', key = 'query', placeholder = 'Ingrese su query').upper()
run = st.button('Run Query')
reset = st.button('Limpiar', on_click = clear_text)

res = cur.execute(query).fetchall()

if res != []:
    data = pd.DataFrame(data = res)
    st.dataframe(data)