import receita
import vendedor
import quantidade_vendas as qt_vendas
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from babel.numbers import format_currency, format_decimal

# Nomes das colunas
LOCAL_COMPRA = 'Local da compra'
DATA_COMPRA = 'Data da Compra'
CATEGORIA_PRODUTO = 'Categoria do Produto'
PRECO = 'Preço'
ANO = 'Ano'
MES = 'Mes'

regiao = ''
ano = ''

st.title('DASHBOARD DE VENDAS :shopping_cart:')
st.set_page_config(layout='wide')

url = 'https://labdados.com/produtos'
query_string = {'regiao':regiao.lower(), 'ano':ano}
response = requests.get(url, verify=False, params= query_string)
dados = pd.DataFrame.from_dict(response.json())
dados[DATA_COMPRA] = pd.to_datetime(dados[DATA_COMPRA], format='%d/%m/%Y')

regioes = ['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']
st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox('Região', regioes)
if regiao == 'Brasil':
    regiao = ''
todos_anos = st.sidebar.checkbox('Dados de todo o período', value = True)
if todos_anos:
    ano = ''
else:
    ano = st.sidebar.slider('Ano', 2020, 2023)    
filtro_vendedores = st.sidebar.multiselect('Vendedores', dados['Vendedor'].unique())
if filtro_vendedores:
    dados = dados[dados['Vendedor'].isin(filtro_vendedores)]

def adiciona_cabecalho():
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        total_preco = dados[PRECO].sum()
        st.metric('Receita', format_currency(total_preco, 'BRL', locale='pt_BR'))
    with coluna2:
        st.metric('Quantidade de vendas', format_decimal(dados.shape[0], locale='pt_BR'))        

## Visualização no streamlit
aba1, aba2, aba3, aba4 = st.tabs(['Receita', 'Quantidade de vendas', 'Vendedores', 'Relatório vendas'])

with aba1:
    adiciona_cabecalho()
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(receita.build_grafico_mapa(dados), use_container_width=True)
        st.plotly_chart(receita.build_grafico_barras(dados,LOCAL_COMPRA))
    with coluna2:
        st.plotly_chart(receita.build_grafico_linhas(dados), use_container_width=True)
        st.plotly_chart(receita.build_grafico_barras(dados,CATEGORIA_PRODUTO))

with aba2:
    adiciona_cabecalho()
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(qt_vendas.build_grafico_mapa(dados), key='chartMapaQtde')
        st.plotly_chart(qt_vendas.build_grafico_barras(dados, LOCAL_COMPRA), key='chartBarQtdeLocal')
    with coluna2:
        st.plotly_chart(qt_vendas.build_grafico_linhas(dados), key='chartLineQtde')
        st.plotly_chart(qt_vendas.build_grafico_barras(dados,CATEGORIA_PRODUTO), key='chartBarQtdeCategoria')

with aba3:
    adiciona_cabecalho()
    qtd_vendedores = st.number_input('Quantidade de vendedores', 2, 10, 5)
    
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(vendedor.build_receita_vendedores(dados,qtd_vendedores))
    with coluna2:
        st.plotly_chart(vendedor.build_qtde_vendedores(dados,qtd_vendedores))

with aba4:
    st.dataframe(
        dados,
        column_config={
            DATA_COMPRA: st.column_config.DateColumn(
                "Data de Compra",
                format="DD/MM/YYYY",  # Formato de exibição visual
            )
        }
    )