import streamlit as st 
import requests
import json
import pandas as pd
from pandas import json_normalize
from io import StringIO
from sqlalchemy import create_engine
import plotly.express as px
import random
import plotly.figure_factory as ff
st.title('AP2 Web Data Applications')

st.header('Douglas Felipe - 2303767, Maria Vitoria - 2401714  and Willian Fagundes - 2401648')
tab1, tab2, tab3, tab4, tab5, tab6,tab7 = st.tabs(["Nomes", "Tipos", "Valores_Com_Desconto", "Valores_Sem_Desconto", "Porcentagem_Desconto", "Avaliações", "Modelos"])

engine = create_engine('sqlite:///4_Scripts/banconike.db', echo =True)

dados = pd.read_sql('SELECT * FROM dados', con = engine)

def gerar_cores_aleatorias(n):
        return ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
    
cores_aleatorias = gerar_cores_aleatorias(len(dados))

with tab1:
    nome = dados["Nome"].tolist()
    selecionar = st.selectbox("Escolha um nome", nome)
    nomeselecionado = dados[dados["Nome"] == selecionar]
    st.write("Detalhes para o nome selecionado:")
    st.write(nomeselecionado)
    
with tab2:
    tipos = dados["Tipo"]
    frequencia = dados["Tipo"].value_counts()
    desconto = dados["Tipo"].value_counts()
    desc = dados[['Tipo','Porcentagem desc']]
    desc_media = desc.groupby(desc['Tipo']).mean().round(2)
    valores = dados[["Tipo","Valor c desc"]]
    valores_media = valores.groupby(valores['Tipo']).mean().round(2)
    nota = dados[["Tipo","Avaliacao"]]
    nota_media = nota.groupby(nota[nota.columns[0]]).mean().round(2)

    with st.expander("Veja os gráficos"):
        fig_tipo = px.pie(frequencia, 
             names=frequencia.index,
             values=frequencia,
             title="Distribuição dos tipos",  
             width=1000, height=1000)
        fig_desc = px.bar(desc_media, x = desc_media.index, y = desc_media[desc_media.columns[0]], title= "Media de desconto concedido por tipo",
                        color = desc_media.index, color_discrete_sequence=cores_aleatorias, text = desc_media[desc_media.columns[0]])

        fig_media = px.bar(valores_media, x = valores_media.index, y = valores_media[valores_media.columns[0]], 
                           color = valores_media.index,
                           color_discrete_sequence=cores_aleatorias,
                           title= "Media do valor com desconto por tipo",
                           text=valores_media[valores_media.columns[0]])
        fig_media.update_layout(width=1000,height=700,
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=True))

        fig_nota = px.bar(nota_media, x = nota_media.index, y = nota_media[nota_media.columns[0]],
                          title= "Media de avaliações por tipo", color=nota_media.index, color_discrete_sequence=cores_aleatorias,
                          text=nota_media[nota_media.columns[0]])
        fig_nota.update_layout(width=1000, height=700,
                           xaxis=dict(showgrid=True),
                           yaxis=dict(showgrid=False))
            
        st.write("Distribuição dos tipos de roupas coletados na amostra")
        st.plotly_chart(fig_tipo, key='Unique_key_1')
        st.write("Conseguimos ver atraves desse grafico que os tipos de produtos que tem a maior media são do tipo: 'Cardigan', 'Jordan', 'Polo'. E os que tem a pior media de avaliação são do tipo: 'Agasalho','Sunga','Shorts'")
        st.plotly_chart(fig_nota, key='Unique_key_2')
        st.write("Conseguimos ver atraves desse grafico que os tipos de produtos que tem a maior media de preço são do tipo: 'Jaqueta', 'Blusão', 'Agasalho'. E os que tem a menor media de valor são do tipo: 'Meia','Sunga'")
        st.plotly_chart(fig_media, key='Unique_key_3')
        st.write("Conseguimos ver atraves desse grafico que os tipos de produtos que tem a maior media de desconto são do tipo: 'Agasalho'. E os que tem a menor media de valor são do tipo: 'Jordan','Sunga'")
        st.plotly_chart(fig_desc, key= 'Unique_key4')
        
    with st.expander("Veja as tabelas"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Media de descontos",desc_media)
        with col2:
            st.write("Media de avaliações",nota_media)
        with col3:
            st.write("Media de valores com desconto",valores_media)

with tab3:
    valores_com_desconto = {'media': dados['Valor c desc'].mean(),
                            'mediana': dados['Valor c desc'].median(),
                            'maximo': dados['Valor c desc'].max(),
                            'minimo': dados['Valor c desc'].min(),
                            'moda': dados['Valor c desc'].mode()[0],
                            'desvio':dados['Valor c desc'].std()}
    valor_com_desconto = pd.DataFrame(valores_com_desconto, index=[0])
    valor_com_desconto = valor_com_desconto.T
    valor_com_desconto[valor_com_desconto.columns[0]] = valor_com_desconto[valor_com_desconto.columns[0]].round(2)
    vlr_model = dados[["Modelo","Valor c desc"]]
    vlr_tipo = dados[["Tipo","Valor c desc"]]
    q01 = vlr_tipo['Valor c desc'].quantile(0.75)
    q02 = vlr_tipo['Valor c desc'].quantile(0.25)
    q1_tipo = pd.DataFrame(vlr_tipo.loc[vlr_tipo['Valor c desc'] >= q01, 'Tipo'].value_counts().round(2))
    q2_tipo = pd.DataFrame(vlr_tipo.loc[vlr_tipo['Valor c desc'] <= q02, 'Tipo'].value_counts().round(2))
    q1_modelo = pd.DataFrame(vlr_model.loc[vlr_model['Valor c desc'] >= q01, 'Modelo'].value_counts().round(2))
    q2_modelo = pd.DataFrame(vlr_model.loc[vlr_model['Valor c desc'] <= q02, 'Modelo'].value_counts().round(2))
    vlr_model = vlr_model.groupby(['Modelo']).mean().round(2)
    vlr_tipo = vlr_tipo.groupby(['Tipo']).mean().round(2)

    with st.expander("Graficos gerais dos valores com desconto"):
        fig_vlr_c_desc = px.bar(valor_com_desconto, x=valor_com_desconto.index, y=valor_com_desconto[valor_com_desconto.columns[0]],
                      color=valor_com_desconto.index,
                    color_discrete_sequence=cores_aleatorias,
                    text=valor_com_desconto[valor_com_desconto.columns[0]])
        fig_vlr_c_desc.update_layout(
            title='Grafico geral',
            title_font_size=24,
            width = 1000,
            height = 600,          
            )
        st.write("Com esse grafico conseguimos ver as informações de média, mediana, moda, mais barato, mais caro e desvio padrão.")
        st.plotly_chart(fig_vlr_c_desc,key='Unique_key_5')

    with st.expander('Graficos de valores com desconto por Modelo'):
        fig_vlr_model = px.bar(vlr_model, x = vlr_model.index,
                                y=vlr_model[vlr_model.columns[0]],
                                color=vlr_model.index, color_discrete_sequence=cores_aleatorias,
                                text=vlr_model[vlr_model.columns[0]]
                                )        
        fig_q1_vlr =  px.bar(q1_modelo, y= q1_modelo.index,
                                x=q1_modelo[q1_modelo.columns[0]],
                                color=q1_modelo.index, color_discrete_sequence=cores_aleatorias,
                                text_auto=True
                                )
        fig_q2_vlr =  px.pie(q2_modelo, names= q2_modelo.index,
                                values=q2_modelo[q2_modelo.columns[0]],
                                )
        fig_vlr_model.update_layout(
        title='Média de valores por modelo',
        title_font_size=24,
        width = 1000,
        height = 600,              
        )
        fig_q1_vlr.update_layout(
        title='Maior presença no quartil superior',
        title_font_size=14,
        width = 1100,
        height = 600,
        xaxis=dict(
        showgrid=True  
            ),
        yaxis=dict(
        showgrid=False,
        gridcolor='lightgray', 
        gridwidth=1          
            )        
        )
        fig_q2_vlr.update_layout(
        title='Maior presença no quartil inferior',
        title_font_size=14,
        width = 1000,
        height = 600,           
        )
        fig_q2_vlr.update_traces(textinfo='value', textfont=dict(size=14))
        st.write("Verificamos com esse grafico que os modelos: Basquete, para jogar tenis e casual são os que tem a maior media de preço")
        st.write("Os Modelos que tem a menor media de valor: treino academia, skateboarding, yoga")
        st.plotly_chart(fig_vlr_model, key='Unique_key_34')
        st.write("Os modelos que ficam entre os mais caros são: Casual, Futebol, corrida")
        st.plotly_chart(fig_q1_vlr, key='Unique_key_35')
        st.write("Os modelos que ficam entre os mais baratos são: Casual, Futebol, corrida")
        st.plotly_chart(fig_q2_vlr, key='Unique_key_36')
    with st.expander('Graficos de valores com desconto por Tipo'):
        fig_vlr_tipo = px.bar(vlr_tipo, x = vlr_tipo.index,
                                y=vlr_tipo[vlr_tipo.columns[0]],
                                color=vlr_tipo.index, color_discrete_sequence=cores_aleatorias,
                                text=vlr_tipo[vlr_tipo.columns[0]]
                                )        
        fig_q1_vlr_tipo =  px.pie(q1_tipo, names= q1_tipo.index,
                                values=q1_tipo[q1_tipo.columns[0]],
                                
                                )
        fig_q2_vlr_tipo =  px.histogram(q2_tipo, x= q2_tipo.index,
                                y=q2_tipo[q2_tipo.columns[0]],
                                color=q2_tipo.index, color_discrete_sequence=cores_aleatorias,
                                text_auto=True
                                )
        fig_vlr_tipo.update_layout(
        title='Média de valores por Tipo',
        title_font_size=24,
        width = 1000,
        height = 600,              
        )
        fig_q1_vlr_tipo.update_layout(title='Maior presença no quartil superior',
        title_font_size=14,
        width = 1000,
        height = 600, 
          
        )
        fig_q2_vlr_tipo.update_layout(title='Maior presença no quartil inferior',
        title_font_size=14,
        width = 1000,
        height = 600,
        xaxis=dict(
        showgrid=True  
            ),
        yaxis=dict(
        showgrid=True,
        gridcolor='lightgray', 
        gridwidth=1          
            )      
        )
        fig_q1_vlr_tipo.update_traces(textinfo='value', textfont=dict(size=14))
        st.write("Os tipos que tem a maior media de preço com desconto são: Jaqueta, Blusão, Agasalho")
        st.plotly_chart(fig_vlr_tipo, key='Unique_key_37')
        st.write("Os tipos que ficam entre os mais caros são: Jaqueta, Blusão, Camisa")
        st.plotly_chart(fig_q1_vlr_tipo, key='Unique_key_38')
        st.write("Os tipos que ficam entre os mais baratos são: Camiseta, ShortsS")
        st.plotly_chart(fig_q2_vlr_tipo, key='Unique_key_39')
    with st.expander("Veja as tabelas"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Media de valores modelo",vlr_model)
        with col2:
            st.write("Quartil superior modelos",q1_modelo)
        with col3:
            st.write("Quartil inferior",q2_modelo)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Media de valores tipo",vlr_tipo)
        with col2:
            st.write("Quartil superior tipos",q1_tipo)
        with col3:
            st.write("Quartil inferior tipos",q2_tipo)
            
with tab4:
    valores_sem_desconto = {'media': dados['Valor s desc'].mean(),
                            'mediana': dados['Valor s desc'].median(),
                            'maximo': dados['Valor s desc'].max(),
                            'minimo': dados['Valor s desc'].min(),
                            'moda': dados['Valor s desc'].mode()[0],
                            'desvio':dados['Valor s desc'].std()}
    valor_sem_desconto = pd.DataFrame(valores_sem_desconto, index=[0])
    valor_sem_desconto = valor_sem_desconto.T
    valor_sem_desconto[valor_sem_desconto.columns[0]] = valor_sem_desconto[valor_sem_desconto.columns[0]].round(2)
    vlr_model = dados[["Modelo","Valor s desc"]]
    vlr_tipo = dados[["Tipo","Valor s desc"]]
    q01 = vlr_tipo['Valor s desc'].quantile(0.75)
    q02 = vlr_tipo['Valor s desc'].quantile(0.25)
    q1_tipo = pd.DataFrame(vlr_tipo.loc[vlr_tipo['Valor s desc'] >= q01, 'Tipo'].value_counts().round(2))
    q2_tipo = pd.DataFrame(vlr_tipo.loc[vlr_tipo['Valor s desc'] <= q02, 'Tipo'].value_counts().round(2))
    q1_modelo = pd.DataFrame(vlr_model.loc[vlr_model['Valor s desc'] >= q01, 'Modelo'].value_counts().round(2))
    q2_modelo = pd.DataFrame(vlr_model.loc[vlr_model['Valor s desc'] <= q02, 'Modelo'].value_counts().round(2))
    vlr_model = vlr_model.groupby(['Modelo']).mean().round(2)
    vlr_tipo = vlr_tipo.groupby(['Tipo']).mean().round(2)
   
    with st.expander("Graficos gerais dos valores sem desconto"):
        fig_vlr_s_desc = px.bar(valor_sem_desconto, x=valor_sem_desconto.index, y=valor_sem_desconto[valor_sem_desconto.columns[0]],
                                color=valor_sem_desconto.index, color_discrete_sequence=cores_aleatorias,text=valor_sem_desconto[valor_sem_desconto.columns[0]],
                                )
        fig_vlr_s_desc.update_layout(
        title='Grafico geral',
        title_font_size=24,
        width = 1000,
        height = 600,          
        )
        st.write("Com esse grafico conseguimos ver as informações de média, mediana, moda, mais barato, mais caro e desvio padrão.")
        st.plotly_chart(fig_vlr_s_desc,key='Unique_key_6')

    with st.expander('Graficos de valores sem desconto por Modelo'):
        fig_vlr_model = px.bar(vlr_model, x = vlr_model.index,
                                y=vlr_model[vlr_model.columns[0]],
                                color=vlr_model.index, color_discrete_sequence=cores_aleatorias,
                                text=vlr_model[vlr_model.columns[0]]
                                )        
        fig_q1_vlr =  px.histogram(q1_modelo, y= q1_modelo.index,
                                x=q1_modelo[q1_modelo.columns[0]],
                                color=q1_modelo.index, color_discrete_sequence=cores_aleatorias,
                                text_auto=True
                                )
        fig_q2_vlr =  px.pie(q2_modelo, names= q2_modelo.index,
                                values=q2_modelo[q2_modelo.columns[0]],
                                )
        fig_vlr_model.update_layout(
        title='Média de valores por modelo',
        title_font_size=24,
        width = 1000,
        height = 600,              
        )
        fig_q1_vlr.update_layout(
        title='Maior presença no quartil superior',
        title_font_size=14,
        width = 1100,
        height = 600,
        xaxis=dict(
        showgrid=True  
            ),
        yaxis=dict(
        showgrid=False,
        gridcolor='lightgray', 
        gridwidth=1          
            )        
        )
        fig_q2_vlr.update_layout(
        title='Maior presença no quartil inferior',
        title_font_size=14,
        width = 1000,
        height = 600,           
        )
        fig_q2_vlr.update_traces(textinfo='value', textfont=dict(size=14))
        st.write("Os modelos que tem a maior media de preço sem desconto são: Para jogar tenis, basquete, casual")
        st.plotly_chart(fig_vlr_model, key='Unique_key_20')
        st.write("Os modelos que estão entre os mais caros são: Casual, Corrida, Futebol")
        st.plotly_chart(fig_q1_vlr, key='Unique_key_21')
        st.write("Os modelos que estão entre os mais baratos são: casual, Corrida, Futebol")
        st.plotly_chart(fig_q2_vlr, key='Unique_key_22')
    with st.expander('Graficos de valores sem desconto por Tipo'):
        fig_vlr_tipo = px.bar(vlr_tipo, x = vlr_tipo.index,
                                y=vlr_tipo[vlr_tipo.columns[0]],
                                color=vlr_tipo.index, color_discrete_sequence=cores_aleatorias,
                                text=vlr_tipo[vlr_tipo.columns[0]]
                                )        
        fig_q1_vlr_tipo =  px.pie(q1_tipo, names= q1_tipo.index,
                                values=q1_tipo[q1_tipo.columns[0]],
                                
                                )
        fig_q2_vlr_tipo =  px.histogram(q2_tipo, x= q2_tipo.index,
                                y=q2_tipo[q2_tipo.columns[0]],
                                color=q2_tipo.index, color_discrete_sequence=cores_aleatorias,
                                text_auto=True
                                )
        fig_vlr_tipo.update_layout(
        title='Média de valores por Tipo',
        title_font_size=24,
        width = 1000,
        height = 600,              
        )
        fig_q1_vlr_tipo.update_layout(title='Maior presença no quartil superior',
        title_font_size=14,
        width = 1000,
        height = 600, 
          
        )
        fig_q2_vlr_tipo.update_layout(title='Maior presença no quartil inferior',
        title_font_size=14,
        width = 1000,
        height = 600,
        xaxis=dict(
        showgrid=True  
            ),
        yaxis=dict(
        showgrid=True,
        gridcolor='lightgray', 
        gridwidth=1          
            )      
        )
        fig_q1_vlr_tipo.update_traces(textinfo='value', textfont=dict(size=14))
        st.write("Os tipos que tem a maior media de preço sem desconto são: Jaqueta, Polo, Agasalho")
        st.plotly_chart(fig_vlr_tipo, key='Unique_key_30')
        st.write("Os tipos que estão entre os mais caros são: Jaqueta, Blusão, Calça")
        st.plotly_chart(fig_q1_vlr_tipo, key='Unique_key_31')
        st.write("Os tipos que estão entre os mais baratos são: Camisa, Shorts, Meia")
        st.plotly_chart(fig_q2_vlr_tipo, key='Unique_key_32')
    with st.expander("Veja as tabelas"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Media de valores modelo",vlr_model)
        with col2:
            st.write("Quartil superior modelos",q1_modelo)
        with col3:
            st.write("Quartil inferior",q2_modelo)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Media de valores tipo",vlr_tipo)
        with col2:
            st.write("Quartil superior tipos",q1_tipo)
        with col3:
            st.write("Quartil inferior tipos",q2_tipo)
      
with tab5:
    desconto = {'media': dados['Valor s desc'].mean(),
                            'mediana': dados['Valor s desc'].median(),
                            'maximo': dados['Valor s desc'].max(),
                            'minimo': dados['Valor s desc'].min(),
                            'moda': dados['Valor s desc'].mode()[0],
                            'desvio':dados['Valor s desc'].std()}
    desconto = pd.DataFrame(desconto, index = [0])
    desconto= desconto.T
    desc = dados[["Modelo","Porcentagem desc"]]
    desc_model = desc.groupby(['Modelo']).mean()
    desc_tipo = dados[["Tipo","Porcentagem desc"]]
    desc_tipo2 = desc_tipo.groupby(['Tipo']).mean()
    q01 = desc_tipo['Porcentagem desc'].quantile(0.75)
    q02 = desc_tipo['Porcentagem desc'].quantile(0.25)
    st.write(desconto)
    q1_tipo = pd.DataFrame(desc_tipo.loc[desc_tipo['Porcentagem desc'] >= q01, 'Tipo'].value_counts().round(2))
    q2_tipo = pd.DataFrame(desc_tipo.loc[desc_tipo['Porcentagem desc'] <= q02, 'Tipo'].value_counts().round(2))
    q1_modelo = pd.DataFrame(desc.loc[desc['Porcentagem desc'] >= q01, 'Modelo'].value_counts().round(2))
    q2_modelo = pd.DataFrame(desc.loc[desc['Porcentagem desc'] <= q02, 'Modelo'].value_counts().round(2))
    desc_model = desc_model.groupby(['Modelo']).mean().round(2)
    desc_tipo = desc_tipo.groupby(['Tipo']).mean().round(2)
    
    desc_model[desc_model.columns[0]] = desc_model[desc_model.columns[0]].round(2)
    desc_tipo2[desc_tipo2.columns[0]] = desc_tipo2[desc_tipo2.columns[0]].round(2)
    desconto[desconto.columns[0]] = desconto[desconto.columns[0]].round(2)
    
    #with st.expander("Graficos dos valores gerais de descontos"):
    fig_data_desc = px.bar(desconto, x = desconto.index,
                                y = desconto[desconto.columns[0]],
                                color=desconto.index, color_discrete_sequence=cores_aleatorias,
                                text=desconto[desconto.columns[0]])
    fig_data_desc.update_layout(
        title='Grafico geral',
        title_font_size=24,
        width = 1000,
        height = 600)
    st.write("Com esse grafico conseguimos ver as informações de média, mediana, moda, mais barato, mais caro e desvio padrão.")
    st.plotly_chart(fig_data_desc, key='Unique_key_26')
    with st.expander("Graficos de desconto por Modelos"):
        fig_desc_model = px.bar(desc_model, x = desc_model.index,
                                y=desc_model[desc_model.columns[0]],
                                color=desc_model.index, color_discrete_sequence=cores_aleatorias,
                                text= desc_model[desc_model.columns[0]]
                                )        
        fig_q1_modelo =  px.pie(q1_modelo, names= q1_modelo.index,
                                values=q1_modelo[q1_modelo.columns[0]],
                                )
        fig_q2_modelo =  px.pie(q2_modelo, names= q2_modelo.index,
                                values=q2_modelo[q2_modelo.columns[0]],
                                )
        fig_desc_model.update_layout(
        title='Média de desconto',
        title_font_size=24,
        width = 1000,
        height = 600,              
        )
        fig_q1_modelo.update_layout(
        title='Maior presença no quartil superior',
        title_font_size=14,
        width = 1000,
        height = 600,           
        )
        fig_q2_modelo.update_layout(
        title='Maior presença no quartil inferior',
        title_font_size=14,
        width = 1000,
        height = 600,           
        )
        st.write("Os modelos que tem a maior media de desconto são: Para jogar tenis, basquete, treino academia")
        st.plotly_chart(fig_desc_model, key='Unique_key_27')
        st.write("Os modelos que tem maiores descontos: Futebol, Casual, Treino academia")
        st.plotly_chart(fig_q1_modelo, key='Unique_key_28')
        st.write("Os modelos que tem os menores descontos: Casual, Futebol, Corrida")
        st.plotly_chart(fig_q2_modelo, key='Unique_key_29')
    with st.expander("Graficos de desconto por tipo"):        
        fig_desc_tipo = px.bar(desc_tipo2, x = desc_tipo2.index,
                                y=desc_tipo2[desc_tipo2.columns[0]],
                                color=desc_tipo2.index, color_discrete_sequence=cores_aleatorias,
                                text=desc_tipo2[desc_tipo2.columns[0]]
                                )
        fig_q1_tipo =  px.pie(q1_tipo, names= q1_tipo.index,
                                values=q1_tipo[q1_tipo.columns[0]],
                                )
        fig_q2_tipo =  px.pie(q2_tipo, names= q2_tipo.index,
                                values=q2_tipo[q2_tipo.columns[0]],
                                )
        fig_desc_tipo.update_layout(
        title='Média de desconto',
        title_font_size=24,
        width = 1000,
        height = 600,              
        )
        fig_q1_tipo.update_layout(
        title='Maior presença no quartil superior',
        title_font_size=14,
        width = 1000,
        height = 600,           
        )
        fig_q2_tipo.update_layout(
        title='Maior presença no quartil inferior',
        title_font_size=14,
        width = 1000,
        height = 600,           
        )
        st.write("Os tipos que tem a maior media de desconto são: Para jogar tenis, basquete, treino academia")
        st.plotly_chart(fig_desc_tipo, key='Unique_key_23')
        st.write("Os modelos que tem maiores descontos são: Polo, Regata, Jaqueta")
        st.plotly_chart(fig_q1_tipo, key='Unique_key_24')
        st.write("Os modelos que tem os menores descontos são: Para jogar tenis, basquete, treino academia")
        st.plotly_chart(fig_q2_tipo, key='Unique_key_25')
   
    with st.expander("Veja as tabelas"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Media de descontos",desc_model)
        with col2:
            st.write("Quartil superior modelos",q1_modelo)
        with col3:
            st.write("Quartil inferior",q2_modelo)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Media de descontos",desc_tipo2)
        with col2:
            st.write("Quartil superior tipos",q1_tipo)
        with col3:
            st.write("Quartil inferior tipos",q2_tipo)
       
with tab6:
    contagem = dados["Avaliacao"].value_counts()
    contagem= pd.DataFrame(contagem)
    medias = {'media': dados['Avaliacao'].mean(),
                            'mediana': dados['Avaliacao'].median(),
                            'maximo': dados['Avaliacao'].max(),
                            'minimo': dados['Avaliacao'].min(),
                            'moda': dados['Avaliacao'].mode()[0],
                            'desvio':dados['Avaliacao'].std()}
    media = pd.DataFrame(medias, index = [0]).round(2)
    media = media.T
    nota_1 = dados.loc[(dados['Avaliacao'] >= 0) & (dados['Avaliacao'] <=1), 'Nome'].value_counts()
    nota_2 = dados.loc[(dados['Avaliacao'] > 1) & (dados['Avaliacao'] <=2), 'Nome'].value_counts()
    nota_3 = dados.loc[(dados['Avaliacao'] > 2) & (dados['Avaliacao'] <=3), 'Nome'].value_counts()
    nota_4 = dados.loc[(dados['Avaliacao'] > 3) & (dados['Avaliacao'] <=4), 'Nome'].value_counts()
    nota_5 = dados.loc[(dados['Avaliacao'] > 4) & (dados['Avaliacao'] <=5), 'Nome'].value_counts()


    #mostrar os graficos em um expander é legal
    with st.expander("Graficos gerais dos valores de avaliações"):
     
        fig_avalia = px.bar(media,x=media.index, y=media[media.columns[0]],color = media.index, color_discrete_sequence=cores_aleatorias, text=media[media.columns[0]])
        fig_avalia.update_layout(showlegend=False)
        st.write("Com esse grafico conseguimos ver as informações de média, mediana, moda, mais barato, mais caro e desvio padrão.")
        st.plotly_chart(fig_avalia, key= "Unique_key_7")
        fig_tipo = px.pie(contagem, 
             names=contagem.index,
             values=contagem[contagem.columns[0]],
             title="Distribuição de notas", 
             width=1000, height=1000)
        st.write("Com esse grafico conseguimos identificar que a nota mais presente é a nota 5")
        st.plotly_chart(fig_tipo, key='Unique_key_8')

    with st.expander('Graficos das avaliações por Modelo'):
        avaliacao_model = dados[["Modelo","Avaliacao"]]
        avaliacao_model = avaliacao_model.groupby(["Modelo"]).mean().round(2)
        avaliacao_model = pd.DataFrame(avaliacao_model)
        fig_avl_model = px.bar(avaliacao_model, x = avaliacao_model.index,
                                y=avaliacao_model[avaliacao_model.columns[0]],
                                color=avaliacao_model.index, color_discrete_sequence=cores_aleatorias,
                                text=avaliacao_model[avaliacao_model.columns[0]]
                                )        
        fig_q1_avl =  px.histogram(q1_modelo, y= q1_modelo.index,
                                x=q1_modelo[q1_modelo.columns[0]],
                                color=q1_modelo.index, color_discrete_sequence=cores_aleatorias,
                                text_auto=True
                                )
        fig_q2_avl =  px.pie(q2_modelo, names= q2_modelo.index,
                                values=q2_modelo[q2_modelo.columns[0]],
                                )
        fig_avl_model.update_layout(
        title='Média de avaliações por modelo',
        title_font_size=24,
        width = 1000,
        height = 600,              
        )
        fig_q1_avl.update_layout(
        title='Maior presença no quartil superior',
        title_font_size=14,
        width = 1100,
        height = 600,
        xaxis=dict(
        showgrid=True  
            ),
        yaxis=dict(
        showgrid=False,
        gridcolor='lightgray', 
        gridwidth=1          
            )        
        )
        fig_q2_avl.update_layout(
        title='Maior presença no quartil inferior',
        title_font_size=14,
        width = 1000,
        height = 600,           
        )
        fig_q2_avl.update_traces(textinfo='value', textfont=dict(size=14))
        
        st.write("Conseguimos ver as que as maiores medias de avaliação são dos modelos: Yoga, Casual Skateboarding, Basquete Casual")
        st.plotly_chart(fig_avl_model, key='Unique_key_40')
        st.write("Os modelos que tem a maior quantidade de avaliação são: Casual, Futebol, Corrida")
        st.plotly_chart(fig_q1_avl, key='Unique_key_41')
        st.write("Os modelos que tem a menor quantidade de avaliação são: Casual, Futebol, Corrida")
        st.plotly_chart(fig_q2_avl, key='Unique_key_42')

    with st.expander('Graficos de avaliações por Tipo'):
        avaliacao_tipo = dados[["Tipo","Avaliacao"]]
        avaliacao_tipo = avaliacao_tipo.groupby(["Tipo"]).mean().round(2)
        avaliacao_tipo = pd.DataFrame(avaliacao_tipo)
        st.write(avaliacao_tipo)
        fig_avl_tipo = px.bar(avaliacao_tipo, x = avaliacao_tipo.index,
                                y=avaliacao_tipo[avaliacao_tipo.columns[0]],
                                color=avaliacao_tipo.index, color_discrete_sequence=cores_aleatorias,
                                text=avaliacao_tipo[avaliacao_tipo.columns[0]]
                                )        
        fig_q1_avl_tipo =  px.pie(q1_tipo, names= q1_tipo.index,
                                values=q1_tipo[q1_tipo.columns[0]],
                                
                                )
        fig_q2_avl_tipo =  px.histogram(q2_tipo, x= q2_tipo.index,
                                y=q2_tipo[q2_tipo.columns[0]],
                                color=q2_tipo.index, color_discrete_sequence=cores_aleatorias,
                                text_auto=True
                                )
        fig_avl_tipo.update_layout(
        title='Média de avaliações por Tipo',
        title_font_size=24,
        width = 1000,
        height = 600,              
        )
        fig_q1_avl_tipo.update_layout(title='Maior presença no quartil superior',
        title_font_size=14,
        width = 1000,
        height = 600, 
          
        )
        fig_q2_avl_tipo.update_layout(title='Maior presença no quartil inferior',
        title_font_size=14,
        width = 1000,
        height = 600,
        xaxis=dict(
        showgrid=True  
            ),
        yaxis=dict(
        showgrid=True,
        gridcolor='lightgray', 
        gridwidth=1          
            )      
        )
        fig_q1_avl_tipo.update_traces(textinfo='value', textfont=dict(size=14))
        st.write("Conseguimos ver as que as maiores medias de avaliação são os tipos: Agasalho, legging, cardigan")

        st.plotly_chart(fig_avl_tipo, key='Unique_key_43')
        st.write("Os tipos que tem a maior quantidade de avaliação são: Camiseta, Shorts, camisa")
        st.plotly_chart(fig_q1_avl_tipo, key='Unique_key_44')
        st.write("Os modelos que tem a menor quantidade de avaliação são: Camiseta, Shorts, camisa")
        st.plotly_chart(fig_q2_avl_tipo, key='Unique_key_45')
    with st.expander("Veja as tabelas"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Media de avaliações modelo",avaliacao_model)
        with col2:
            st.write("Quartil superior modelos",q1_modelo)
        with col3:
            st.write("Quartil inferior",q2_modelo)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Media de avaliações tipo",avaliacao_tipo)
        with col2:
            st.write("Quartil superior tipos",q1_tipo)
        with col3:
            st.write("Quartil inferior tipos",q2_tipo)

        selecionar = st.selectbox("Selecione uma nota", ["nota1", "nota2", "nota3", "nota4", "nota5"])
        if selecionar == "nota1":
            st.write("Produtos com avaliação 1",nota_1)
        elif selecionar == "nota2":
            st.write("Produtos com avaliação 2",nota_2)
        elif selecionar == "nota3":
            st.write("Produtos com avaliação 3",nota_3)
        elif selecionar == "nota4":
            st.write("Produtos com avaliação 4",nota_4)
        elif selecionar == "nota5":
            st.write("Produtos com avaliação 5",nota_5)
with tab7:
    
    modelos = dados["Modelo"]
    frequencia = dados["Modelo"].value_counts()
    frequencia = pd.DataFrame(frequencia)
    desconto = dados["Modelo"].value_counts()
    desc = dados[['Modelo','Porcentagem desc']]
    desc_media = desc.groupby(desc['Modelo']).mean().round(2)
    valores = dados[["Modelo","Valor c desc"]]
    valores_media = valores.groupby(valores['Modelo']).mean().round(2)
    nota = dados[["Modelo","Avaliacao"]]
    nota_media = nota.groupby(nota[nota.columns[0]]).mean().round(2)

    with st.expander("Veja os gráficos"):

        fig_Modelo = px.pie(frequencia, 
             names=frequencia.index,
             values=frequencia[frequencia.columns[0]],
             title="Distribuição dos modelos", 
             width=1000, height=1000)

        fig_desc = px.bar(desc_media, x=desc_media.index, y='Porcentagem desc',title="Média de descontos por Modelo",
                        color=valores_media.index, color_discrete_sequence=cores_aleatorias, text = desc_media[desc_media.columns[0]])

        fig_media = px.bar(valores_media, x=valores_media.index, y='Valor c desc',title="Média dos valores com desconto por Modelo",
                        color=valores_media.index, color_discrete_sequence=cores_aleatorias, text = valores_media[valores_media.columns[0]])
        fig_media.update_layout(width=1000,height=700,
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=True))

        fig_nota = px.bar(nota_media, y=nota_media.index, x='Avaliacao',title="Média de avaliações por Modelo",
                        color=nota_media.index, color_discrete_sequence=cores_aleatorias, orientation='h',text = nota_media[nota_media.columns[0]])
        fig_nota.update_layout(width=1000, height=700,
                           xaxis=dict(showgrid=True),
                           yaxis=dict(showgrid=False))

        st.write("Distribuição em porcentagem mostra que os modelos mais presentes são: Casual, Futebol, Corrida")
        st.plotly_chart(fig_Modelo, key='Unique_key_10')
        st.write("Os modelos mais bem avaliados são: Yoga, Casual Skate, Basquete Casual")
        st.plotly_chart(fig_nota, key='Unique_key_11')
        st.write("Os modelos mais caros em media são: Para jogar tenis, Casual Skateboarding, Basquete")
        st.plotly_chart(fig_media, key='Unique_key_12')
        st.write("Os modelos com maior media de desconto são: para jogar tenis, Treino Academia, Basquete")
        st.plotly_chart(fig_desc, key= 'Unique_key13')
    with st.expander("Veja as tabelas"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Media de descontos",desc_media)
        with col2:
            st.write("Media de avaliações",nota_media)
        with col3:
            st.write("Media de valores com desconto",valores_media)




    
   
    

    
        
