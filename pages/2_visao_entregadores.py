#LIBRARIES
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import folium_static
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
st.header("Marketplace - Visão entregadores")
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
tab1,tab2,tab3 = st.tabs(["Visão Gerencial","_","_"])

with tab1:
     with st.container():
         st.title ("Overal Metrics")
         col1,col2,col3,col4 = st.columns(4,gap="large")
         with col1:
             #Maior idade dos entregadores#
              
              Maior_idade = df.loc[:,"Delivery_person_Age"].max()    
              col1.metric("maior de idade", Maior_idade)

         with col2:
             # Menor idade dos entregadores#
              
              Menor_idade=df.loc[:,"Delivery_person_Age"].min()
              col2.metric("menor de idade", Menor_idade)
             
         with col3:
              Melhor_condição = df.loc[:,"Vehicle_condition"].max()
              col3.metric ("melhor condição",Melhor_condição)
             
         with col4:
                 
              Pior_condição = df.loc[:,"Vehicle_condition"].min()
              col4.metric ("pior condição",Pior_condição)
              
             
     with st.container():
         st.markdown("""___""") #linha para dividir os dashboards#
         st.title("Avaliações")
         col1,col2=st.columns(2)
         with col1:
             st.markdown("Avaliação medias por entregador")
             df_avg_ratings_por_deliver=(df.loc[:,["Delivery_person_Ratings","Delivery_person_ID"]]
                                           .groupby("Delivery_person_ID")
                                           .mean()
                                           .reset_index())
             st.dataframe(df_avg_ratings_por_deliver)
             
         with col2:
              st.markdown("Avaliação media por transito")
              df_avg_std_rating_by_traffic =( df.loc[:,["Delivery_person_Ratings","Road_traffic_density"]]
                                             .groupby("Road_traffic_density")
                                             .agg({"Delivery_person_Ratings":  ["mean","std"]}))
             
              #mudança de nome das colunas por conta do index que não e possivel corrigir
              df_avg_std_rating_by_traffic.columns=["delivery_mean","delivery_std"]

              #reset do index
              df_avg_std_rating_by_traffic=df_avg_std_rating_by_traffic.reset_index()

              st.dataframe(df_avg_std_rating_by_traffic)

             
              st.markdown("Avaliação média por clima")
              df_avg_std_rating_by_Weatherconditions = (df.loc[:, ["Delivery_person_Ratings", "Weatherconditions"]]
                                                          .groupby("Weatherconditions")
                                                          .agg({"Delivery_person_Ratings": ["mean", "std"]}))
                                                         

              #mudança de nome das colunas por conta do index que não e possivel corrigir
              df_avg_std_rating_by_Weatherconditions.columns=["delivery_mean","delivery_std"]

              #reset do index
              df_avg_std_rating_by_Weatherconditions= df_avg_std_rating_by_Weatherconditions.reset_index()

              st.dataframe(df_avg_std_rating_by_Weatherconditions)


 

     with st.container():
        st.markdown("""___""")
        st.title("velocidade de entrega")
        col1,col2=st.columns(2)

        with col1:
             st.subheader("top Entregadores mais rapidos")
             df2=(df.loc[:,["Delivery_person_ID","City","Time_taken(min)"]]
                   .groupby(["City","Delivery_person_ID"])
                   .mean()
                   .sort_values(["City","Time_taken(min)"]).reset_index())

            
             df_aux01= df2.loc[df2["City"]=="Metropolitian", :].head(10)
             df_aux02= df2.loc[df2["City"]=="Urban", :].head(10)
             df_aux03= df2.loc[df2["City"]=="Semi-Urban" ,:].head(10)

             #unir as 3 frames
             df3=pd.concat([df_aux01,df_aux02,df_aux03]).reset_index(drop=True)
             st.dataframe(df3)



    
        with col2:
             st.subheader("top entregadores mais lentos")    
             df3=(df.loc[:,["Delivery_person_ID","City","Time_taken(min)"]]
                   .groupby(["City","Delivery_person_ID"])
                   .min()
                   .sort_values(["City","Time_taken(min)"], ascending=False ).reset_index() )

             

            
             df_aux01= df3.loc[df3["City"]=="Metropolitan", :].head(10)
             df_aux02= df3.loc[df3["City"]=="Urban", :].head(10)
             df_aux03= df3.loc[df3["City"]=="Semi-Urban" ,:].head(10)

             #unir as 3 frames
             df4=pd.concat([df_aux01,df_aux02,df_aux03]).reset_index(drop=True)
             st.dataframe(df4)















