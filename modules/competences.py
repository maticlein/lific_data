import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import tempfile
from fpdf import FPDF
from fpdf import enums
import plotly.io as pio
import os


def competences_info():
    st.markdown("- RA1: Proponer diversas alternativas de solución, que sean factibles,  para resolver un desafío planteado a partir de la aplicación de principios teóricos de STEM y el aprendizaje iterativo.")
    st.markdown("- RA2: Experimentar alternativas para resolver un desafío planteado incorporando aspectos éticos y una perspectiva sistémica para su resolución.")
    st.markdown("- RA3: Construir prototipos funcionales para dar respuesta a un desafío planteado atingente al campo disciplinar, justificando sus decisiones a partir de los fundamentos del ciclo básico")

    st.subheader('Innovación')
    with st.expander("Problemática"):
        st.write("1.1 Define un problema y sus objetivos a partir del contexto del reto planteado a partir de la búsqueda de información asociada.")
        st.write("1.2 Valida la problemática con los usuarios potenciales utilizando herramientas afínes.")
        st.write("1.3 Busca información sobre el tema propuesto para contextualizar y sustentar su trabajo.")
    with st.expander("Propuesta de la Solución"):
        st.write("1.4 Identifica principios STEM en la propuesta de la solución del reto planteado.")
        st.write("1.5 Planifica las actividades a realizar y presupuesto para el desarrollo de la solución propuesta.")
        st.write("1.6 Define una propuesta de solución acorde a la problemática incorporando elementos de monitoreo, control y herramientas de prototipado.")
        st.write("1.7 Elabora un boceto de su propuesta de solución incorporando los elementos mínimos solicitados.")

    with st.expander('Comunicación'):
        st.write("1.8 Elabora un anteproyecto que incluye las dimensiones solicitadas para la solución.")

    st.subheader('Responsabilidad Social')
    with st.expander("Solución"):
        st.write("2.1 Demuestra conceptualmente su propuesta de solución, justificando la viabilidad del mismo.")
        st.write("2.2 Evalúa las propuestas de solución con usuarios potenciales del problema identificado.")
    with st.expander("Comportamiento Ético"):
        st.write("2.3 Respeta las normativas legales vigentes en las funciones que le corresponde desempeñar.")
        st.write("2.4 Evalúa el impacto que tendrá las acciones a ejecutar en las personas y su entorno social.")
    with st.expander("Comunicación"):
        st.write("2.5. Comunica efectivamente los resultados del proceso de experimentación, incluyendo las alternativas consideradas, los análisis éticos y sistémicos realizados incluyendo conclusiones y recomendaciones resultantes.")

    st.subheader('Diseño')
    with st.expander("Prototipo"):
        st.write("3.1 Utiliza herramientas de prototipado para desarrollar una propuesta de solución que sea viable y efectiva para abordar el problema planteado.")
        st.write("3.2 Utiliza herramientas, elementos de protección personal y materiales adecuados para la elaboración de un prototipo funcional.")
        st.write("3.3 Demuestra de manera efectiva el funcionamiento práctico de su prototipo, estableciendo una clara conexión con los conceptos teóricos presentados previamente.")
        st.write("3.4 Realiza iteraciones en su solución, efectuando ajustes y modificaciones para garantizar el funcionamiento del prototipo.")
        st.write("3.5 Evalúa el impacto ambiental causado por los materiales del prototipo mediante el analisis de Ciclo de Vida.")
    with st.expander("Trabajo en equipo"):
        st.write("3.6 Cumple de manera efectiva y consistente con los acuerdos y compromisos establecidos dentro del equipo de trabajo, contribuyendo significativamente al desarrollo exitoso de las tareas asignadas.")
    with st.expander("Comunicación"):
        st.write("3.7 Presenta la solución propuesta ante las y los docentes y sus pares indicando las iteraciones realizadas y el análisis de Ciclo de Vida de los materiales.")

def competences_sunburst_plot():
    data_sunburst_plot = dict(
    elements=["Diseño", "Innovación", "Resp Social", 
            "RA1", "RA2", "RA3", 
            "Problemática", "Propuesta de Solución", "Documentación",
            "Solución", "Comportamiento Ético", "Comunicación",
            "Prototipo", "Trabajo Colaborativo", "Presentación"],
    parent=["", "", "", "Innovación", "Resp Social", "Diseño", "RA1", "RA1", "RA1", "RA2", "RA2", "RA2", "RA3", "RA3", "RA3"],
    value=[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
    )
    fig = px.sunburst(
        data_sunburst_plot,
        names='elements',   
        parents='parent',
        values='value',
    )
    return fig

def progress_plot(progress, competence):
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = progress,
    number = { "suffix": "%" },
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': competence},
    gauge = {
        'axis': {'range': [0, 100], "tickmode": "auto", "nticks": 10, 'tickcolor': "darkblue"},
        'bar': {'color': "#1B5FAA"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 30], 'color': '#d93452'},
            {'range': [31, 60], 'color': '#fa6f4e'},
            {'range': [61, 90], 'color': '#fbc409'},
            {'range': [91, 100], 'color': '#34c077'}
            ]
        }))
    return fig

def competence_result(progress, competence):
    if progress <= 30:
        pos = 0
    elif progress <= 60:
        pos = 1
    elif progress <=90:
        pos = 2
    else:
        pos = 3
    design_results = ["El/la estudiante ha realizado algunos intentos para construir un sistema de cultivo automatizado, pero aún no ha logrado desarrollar un prototipo funcional que aborde adecuadamente el desafío planteado. Las decisiones tomadas carecen de una justificación basada en los aprendizajes del ciclo básico.", 
                      "El/la estudiante ha construido un sistema de cultivo automatizado como prototipo, pero con algunas limitaciones en su funcionalidad. Aunque ha logrado abordar parcialmente el desafío planteado, la justificación de las decisiones tomadas puede ser limitadas o poco fundamentadas en los aprendizajes del ciclo básico y los elementos STEM. Se observan oportunidades de mejora en el desarrollo de la competencia.", 
                      "El/la estudiante ha logrado construir un sistema de cultivo automatizado como prototipo funcional, abordando el desafío planteado de manera satisfactoria. Ha justificado algunas de sus decisiones aplicando aprendizajes del ciclo básico y los elementos STEM. Aunque puede haber áreas de mejora, el estudiante ha demostrado un nivel adecuado de comprensión y aplicación de los conceptos clave.", 
                      "El/ La estudiante demuestra un desarrollo consolidado de la competencia por cuanto logró construir un sistema de cultivo automatizado, como prototipo funcional, para dar respuesta al  desafío planteado, justificando sus decisiones a partir de los aprendizajes obtenidos en el ciclo básico, donde se incluyen las primeras tres asignaturas de la LIFIC, y se desarrollaron elementos STEM, que se visibilizan en el trabajo realizado."]
    innovation_results = ["El/la estudiante muestra un desarrollo incipiente de la competencia. La solución presentada es poco elaborada y hay carencias evidentes en la definición del problema y en el planteamiento de los objetivos del desafío planteado. Aunque se ha hecho un intento, se requiere un mayor esfuerzo para lograr una propuesta integral y respaldada por un boceto adecuado.", 
                          "El/la estudiante demuestra un desarrollo básico de la competencia al presentar una solución respaldada por un boceto. Sin embargo, existen algunas dificultades en la definición precisa del problema y en el planteamiento de los objetivos del desafío. Aunque se han dado los primeros pasos, aún se requiere un mayor nivel de profundidad y detalle en la propuesta.", 
                          "El/la estudiante muestra un desarrollo adecuado de la competencia al proponer una solución parcial respaldada por un boceto. Aunque aún hay un margen de mejora, el/la estudiante ha logrado definir el problema de manera clara y plantear algunos objetivos relacionados con el desafío planteado.", 
                          "El/la estudiante demuestra un desarrollo consolidado de la competencia por cuanto propone una solución integral, respaldada por un boceto, a partir de la definición de un problema y el establecimiento claro de los objetivos relacionados con el desafío planteado."]
    social_resp_results = ["El/la estudiante demuestra un desarrollo incipiente de la competencia, debido a que es incapaz de validar conceptualmente las propuestas de solución. Además, no muestra respeto por las normativas legales vigentes y no evalúa el impacto que tendrán sus acciones en las personas y su entorno social.", 
                           "El/la estudiante demuestra un desarrollo básico de la competencia, ya que puede validar conceptualmente algunas propuestas de solución, pero no todas. Aunque muestra cierto conocimiento de las normativas legales vigentes, no las respeta en su trabajo. Además, evalúa parcialmente el impacto de sus acciones en las personas y su entorno social.", 
                           "El/la estudiante demuestra un desarrollo adecuado de la competencia, ya que valida conceptualmente la mayoría de las propuestas de solución. Respeta en gran medida las normativas legales vigentes y evalúa adecuadamente el impacto que tendrán sus acciones en las personas y su entorno social. Sin embargo, puede haber algunas ocasiones en las que no logre hacerlo de manera consistente.", 
                           "El/ La estudiante demuestra un desarrollo consolidado de la competencia por cuanto valida conceptualmente las propuestas de solución, respetando las normativas legales vigentes y evaluando de manera integral el impacto que tendrá sus acciones en las personas y su entorno social."]
    if competence == "Diseño":
        return design_results[pos]
    elif competence == 'Innovación':
        return innovation_results[pos]
    elif competence == 'Responsabilidad Social':
        return social_resp_results[pos]
    else:
        return "Sin información"
    
def generate_report(option, group, design, innovation, social_resp):
    temp_file = tempfile.NamedTemporaryFile(delete = False, suffix = '.pdf')
    temporary_location = temp_file.name
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margin(20)
    pdf.set_top_margin(30)
    pdf.set_font("Arial", size = 15)
    pdf.image('./img/logo_innovacion.png', x = 95, y = 10, w = 20, h = 20)
    pdf.cell(h = 15, w = 150, new_x = 'LEFT', new_y = 'NEXT')
    pdf.cell(txt = f"**Reporte de Resultados - Taller de Diseño de Ingeniería**", center = True, new_x = 'LEFT', new_y = 'NEXT', markdown = True)
    pdf.cell(txt = f"**{option}**", center = True, new_x = 'LMARGIN', new_y = 'NEXT', markdown = True)

    pdf.set_font("Arial", size = 10)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image1:
        tmp_filename1 = temp_image1.name
        pio.write_image(progress_plot(design, "Diseño"), tmp_filename1)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image2:
        tmp_filename2 = temp_image2.name
        pio.write_image(progress_plot(innovation, "Innovación"), tmp_filename2)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image3:
        tmp_filename3 = temp_image3.name
        pio.write_image(progress_plot(social_resp, "Responsabilidad Social"), tmp_filename3)
    pdf.image(tmp_filename1, w=75, x = enums.Align.C)
    pdf.multi_cell(w = 0, txt = competence_result(design, 'Diseño'), new_x = 'LEFT', new_y = 'NEXT')
    pdf.image(tmp_filename2, w=75, x = enums.Align.C)
    pdf.multi_cell(w = 0, txt = competence_result(innovation, 'Innovación'), new_x = 'LEFT', new_y = 'NEXT')
    pdf.image(tmp_filename3, w=75, x = enums.Align.C)
    pdf.multi_cell(w = 0, txt = competence_result(social_resp, 'Responsabilidad Social'), new_x = 'LEFT', new_y = 'NEXT')
    pdf.output(temporary_location)
    with open(temporary_location, "rb") as file:
        st.download_button(label = 'Descargar reporte', data = file, file_name = f"resultados_grupo{group}.pdf")
    os.remove(temporary_location)
    os.remove(tmp_filename1)
    os.remove(tmp_filename2)
    os.remove(tmp_filename3)

def group_comparison(data, options):
    fig = go.Figure()
    for i in range(0, len(options)):
        group = int(options[i].split()[1])
        datos = data[data['grupo'] == group]
        design = list(datos["diseno"])[0]
        innovation = list(datos["innovacion"])[0]
        social_resp = list(datos["resp_social"])[0]
        fig.add_trace(go.Scatterpolar(
        r = [design, innovation, social_resp],
        theta = ["Diseño", 'Innovación', "Resp. Social"],
        name = options[i],
        showlegend=True
    ))
    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 100]
        )),
    title='Comparación de Grupos'
    )
    return fig