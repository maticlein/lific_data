import streamlit as st
from PIL import Image
import sqlite3
import pandas as pd

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

st.header('Estudiantes por carrera')

query = "SELECT carrera, COUNT(*) as estudiantes_totales FROM estudiantes GROUP BY carrera ORDER BY estudiantes_totales DESC"
res = cur.execute(query).fetchall()

data = pd.DataFrame(res, columns = ['Carrera', 'Cantidad'])

st.dataframe(data = data)