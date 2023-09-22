import streamlit as st
from PIL import Image
page_icon = "\U0001F573"

st.set_page_config(
    page_title = "Home",
    page_icon = "page_icon"
)

##image_path = r"C:\Users\Caio\Documents\cientista de dados\phyton\Ciclo 5\imagem2.jpg"
image = Image.open ("imagem2.jpg")
st.sidebar.image ( image, width = 120)

st.sidebar.markdown("# cury Company")
st.sidebar.markdown("## Fastest delivery in town")
st.sidebar.markdown("""---""")

st.write ( "# Curry Company Growth Dashboard")

st.markdown(
    """ Growth Dashboard foi construido para acompanhar as métricas de crescimento dos entregadores e Empresa.
    ### Como utilizar esse Growth Dashboard?

    - Visão Empresa:
    
    - Visão gerencial: Metricas gerais de comportamento
    - Visão tática: indicadores semanais de crescimento 
    - Visão Geográfica : Insights de geolocalização.

    - Visão Entregador:
    - acompanhamento dos indicadores semanais de crescimento

    ## Ask for help 

    Caio Rodrigues

    """)


    
    