import streamlit as st
from PIL import Image
import sqlite3

favicon = Image.open('./img/logo_innovacion.png')
st.set_page_config(
    page_title = "LIFIC Data - Docentes",
    page_icon = favicon 
)

logos = Image.open('./img/logos_UFRO.png')
st.image(logos, width = 400)
st.title('LIFIC - Línea Integradora de Formación en Ingeniería y Ciencias')

con = sqlite3.connect("./data/lific.db")
cur = con.cursor()

query = "SELECT * FROM docentes"
res = cur.execute(query).fetchall()

for docente in res:
    col1, col2 = st.columns(2)
    with col1:
        if docente[4] == 'Femenino':
            icon = Image.open('./img/icon_woman.png')
        else:
            icon = Image.open('./img/icon_man.png')
        st.image(icon, width = 250)
            
    with col2:
        st.header(docente[1] + ' ' + docente[2] + ' ' + docente[3])
        st.header(docente[5])
        st.header(docente[6])
    st.text("")