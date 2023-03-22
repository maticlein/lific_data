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
    st.markdown('Para todas las Ingenierías Civiles de la Universidad de La Frontera se incorpora una línea formativa denominada Línea Integradora de Formación en Ingeniería y Ciencias (LIFIC), la que presenta las siguientes competencias:\n - Diseño\n- Innovación\n- Responsabilidad Social')    
    lific = Image.open('./img/lific.png')
    st.image(lific)

if __name__ == "__main__":
    main()