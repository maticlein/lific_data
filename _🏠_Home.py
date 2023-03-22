import streamlit as st
from PIL import Image

favicon = Image.open('./img/logo_innovacion.png')
st.set_page_config(
    page_title = "LIFIC Data - Home",
    page_icon = favicon 
)

def main():
    logos = Image.open('./img/logos_UFRO.png')
    st.image(logos, width = 400)
    st.title('LIFIC - Línea Integradora de Formación en Ingeniería y Ciencias')

if __name__ == "__main__":
    main()