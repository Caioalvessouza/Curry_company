#LIBRARIES
import pandas as pd
import numpy as np
import plotly.express as px
import folium
##from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
##(biblioteca para buscar imagem dentro do notebook)
from PIL import Image
#pip install haversine
from haversine import haversine
# Importe o módulo de expressões regulares
import re
#IMPORTAR DIRETO DO COMPUTADOR
df = pd.read_csv('C:/Users/Caio/Documents/cientista de dados/phyton/Ciclo 5/train.crdownload')

#------------------------------------------------------------------------------------------------
# funções
#-----------------------------------------------------------------------------------------------

def clean_code(df):
    
    """ Esta função tem a responsabilidade de limpar o dataframe 
        tipos de limpeza:
        remoção dos dados NaN
        mudança do tipo da coluna de dados
        remoção dos espaços das variaveis de texto
        formatação da data
        limpeza da coluna tempo ( remoção da variavel da numerica)

        input:  dataframe
        output: dataframe  
    """

    # Excluir as linhas com a idade dos entregadores vazia
    # ( Conceitos de seleção condicional )
    linhas_vazias = df['Delivery_person_Age'] != 'NaN '
    df = df.loc[linhas_vazias, :]
    # Conversao de texto/categoria/string para numeros inteiros
    df['Delivery_person_Age'] = df['Delivery_person_Age'].astype( int )
    
    # Conversao de texto/categoria/strings para numeros decimais
    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype( float )
    
    # Conversao de texto para data
    df['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )
    
    def extract_numbers(text):
        if isinstance(text, str):  # Verifica se é uma string antes de aplicar a transformação
            return ''.join(filter(str.isdigit, text))
        else:
            return '0'
    
    # Aplica a função de extração à coluna "Time_taken(min)"
    df["Time_taken(min)"] = df["Time_taken(min)"].apply(extract_numbers)
    
    
    # convertendo multiple_deliveries de texto para numero int
    #linhas_vazias = (df["multiple_deliveries"] != " NaN " )
    #df = df.loc[linhas_vazias, :].copy()
    #df['multiple_deliveries'] = df['multiple_deliveries'].astype( int )
    
    # Substituir os valores NaN por 0
    #df['multiple_deliveries'] = df['multiple_deliveries'].fillna(0).replace("NaN",0)
    
    # Remover espaços em branco do início e do final das strings
    #df['multiple_deliveries'] = df['multiple_deliveries'].str.strip()
    
    # Converter a coluna para o tipo inteiro (int)
    #df['multiple_deliveries'] = df['multiple_deliveries'].astype(int)
    
    
    # Substituir possíveis representações literais de 'NaN' pelo valor real de NaN
    df['multiple_deliveries'] = df['multiple_deliveries'].replace('NaN', np.nan)
    
    # Converter a coluna para o tipo inteiro (int) e preencher os valores NaN com 0
    df['multiple_deliveries'] = df['multiple_deliveries'].astype(float).fillna(0).astype(int)
    
    # removendo os espaços dentro de strings/texto/object
    df.loc[:, "ID"] =df.loc[:, "ID"].str.strip()
    df.loc[:, "Road_traffic_density"] =df.loc[:, "Road_traffic_density"].str.strip()
    df.loc[:, "Type_of_order"] =df.loc[:, "Type_of_order"].str.strip()
    df.loc[:, "Type_of_vehicle"] =df.loc[:, "Type_of_vehicle"].str.strip()
    #df.loc[:, "multiple_deliveries"] =df.loc[:, "multiple_deliveries"].str.strip()
    df.loc[:, "City"] =df.loc[:, "City"].str.strip()


    return df
#----------------------- inicio da estrutura de codigo ---------------------------------------------------
#=========================================================================================================
#==========================
#limpando os dados
#=========================
df = clean_code(df)


    
#VISÃO EMPRESA

#1. Quantidade de pedidos por dia?

#Saída: Um gráfico de barra com a quantidade de entregas no eixo Y e os dias
#no eixo X.

#Processo: Fazer um contagem da colunas “ID” agrupado “Order Date” e usar
#uma bibliotecas de visualização para mostrar o gráfico de barras.

#Entrada: Eu posso usar o comando groupby() para agrupar os dados e o
#comando count() para contar a coluna de IDs e um comando para desenhar
#um gráfico de barras.

# Quantidade de pedidos por dia
df_aux = df.loc[:, ['ID', 'Order_Date']].groupby( 'Order_Date' ).count().reset_index()
# criar um dataframe para criação do gráfico
df_aux.columns = ['data pedidos', 'quantidade entregas'] #ou ['order_date', 'ID'] apenas renomeado

# gráfico
px.bar( df_aux, x='data pedidos', y='quantidade entregas' ) #ou [x='order_date', y='ID']

# Resolução de exercício após visualização da aula

#Quantidade de pedidos por dia?
# quantidade de pedidos "ID"
# dias Order_Date

quantidade_pedidos = df.loc[:, ["ID","Order_Date"]].groupby("Order_Date").count()

#colunas_complementares
df_complementares = ["Order_Date", "ID"]

traffic_options = st.sidebar.multiselect("Quais as condições do trânsito",
    ["Low", "Medium", "High", "Jam"],
    default=["Low", "Medium", "High", "Jam"])

st.sidebar.markdown("___")
st.sidebar.markdown("### Comunidade DS")


#gráfico
px.bar( df_aux, x='data pedidos', y='quantidade entregas' ) #ou [x='order_date', y='ID'].reset_index()

#========================================================================================================

# LEYOUT da pagina lateral

#=========================================================================================================
st.header("Marketplace - Visão Cliente")
#image_path = r"C:\Users\Caio\Documents\cientista de dados\phyton\Ciclo 5\imagem2.jpg"
image = Image.open ("imagem2.jpg")        
st.sidebar.image(image, width=120)
st.sidebar.markdown("# cury Company")
st.sidebar.markdown("## Fastest delivery in town")
st.sidebar.markdown("""---""")
st.sidebar.markdown("## Selecione uma data limite")
##st.header('This is a header')
date_slider = st.sidebar.slider (
    "ate qual valor ?",
value = datetime (2022,4,13),
min_value =datetime(2022, 2, 11),
max_value =datetime (2022,4,6),
format = ("DD-MM-YYYY"))
st.sidebar.markdown("""___""")
print(df.head)
#comando para gerar filtragem em todos os dados do dashboard (data)
linhas_selecionadas=df["Order_Date"] <date_slider
df=df.loc[linhas_selecionadas,:]
#comando para filtrar o transito
linhas_selecionadas=df["Road_traffic_density"].isin(traffic_options)
df=df.loc[linhas_selecionadas,:]
#========================================================================================================

# LEYOUT no streamlit

#=========================================================================================================

tab1,tab2,tab3 = st.tabs(["Visão Gerencial","Visão Tática","Visão Geográfica"])

with tab1:
    with st.container():   
        #order matric
       st.markdown ("# Orders by Day")
       def order_metric (df):
        df_aux = df.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
        fig = px.bar( df_aux, x="Order_Date", y="ID")
        st.plotly_chart(fig, use_container_width=True)    
                
        return fig
#---------------------------------------------------------------------------------------------------                  
    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.header("Traffic Order density")
            
            columns = ["ID","Road_traffic_density"]
            df.aux =df.loc[:,columns].groupby("Road_traffic_density").count().reset_index()
            print(df.aux)
    #criar gráfico
    fig = px.pie( df.aux, values='ID', names='Road_traffic_density' )
    st.plotly_chart(fig, use_container_width=True)

    with col2:
            st.header("Traffic Order City density")
            df_aux = df.loc[:,["ID","City","Road_traffic_density"]].groupby(["City","Road_traffic_density"]).count().reset_index()
            df_aux = df.groupby(["City", "Road_traffic_density"]).size().reset_index(name="Count")
            fig = px.scatter(df_aux, x="City", y="Road_traffic_density", size="Count", color="City")
            fig.show()
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    with st.container():
         st.markdown("# Order by week")
         # criar a Quantidade de pedidos por Semana utilizando o week of year
         df['week_of_year'] = df['Order_Date'].dt.strftime( "%U" )
         df_aux1 = df.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year').count().reset_index()
         df_aux2 = df.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
         df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
         df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
         print(df_aux)
         fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )        
         st.plotly_chart(fig, use_container_width=True)

    with st.container():
          st.markdown("# Order share by week")
          df_aux = df.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
          df_aux = df.loc[:,["ID","week_of_year"]].groupby("week_of_year").count().reset_index()
          fig = px.bar(df_aux, x = "week_of_year" , y="ID" )
          st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("# Country Maps")
    columns = [
        'City',
        'Road_traffic_density',
        'Delivery_location_latitude',
        'Delivery_location_longitude'
    ]
    columns_groupby = ['City', 'Road_traffic_density']
    data_plot = df.loc[:, columns].groupby(columns_groupby).median().reset_index()
    data_plot = data_plot[data_plot['City'] != 'NaN']
    data_plot = data_plot[data_plot['Road_traffic_density'] != 'NaN']
    map_ = folium.Map(zoom_start=8)
    for index, location_info in data_plot.iterrows():
        folium.Marker(
            [location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']],
            popup=location_info[['City', 'Road_traffic_density']]
        ).add_to(map_)
    folium_static(map_, width=1024, height=600)














