import streamlit as st
import requests
import pandas as pd
import time
from constants import *

@st.cache_data
def converte_csv(df):
    return df.to_csv(index = False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!', icon = "✅")
    time.sleep(5)
    sucesso.empty()

st.title('Dados Brutos')
st.set_page_config(layout='wide')

url = 'https://labdados.com/produtos'
response = requests.get(url, verify=False)
dados = pd.DataFrame.from_dict(response.json())
dados[DATA_COMPRA] = pd.to_datetime(dados[DATA_COMPRA], format='%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', dados[PRODUTO].unique(), dados[PRODUTO].unique())
with st.sidebar.expander(CATEGORIA_PRODUTO):
    categorias = st.multiselect('Selecione as categorias', dados[CATEGORIA_PRODUTO].unique(), dados[CATEGORIA_PRODUTO].unique())
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0,5000))
with st.sidebar.expander(FRETE):
    frete = st.slider('Frete', 0,250, (0,250))
with st.sidebar.expander(DATA_COMPRA):
    data_compra = st.date_input('Selecione a data', (dados[DATA_COMPRA].min(), dados[DATA_COMPRA].max()))
with st.sidebar.expander(VENDEDOR):
    vendedores = st.multiselect('Selecione os vendedores', dados[VENDEDOR].unique(), dados[VENDEDOR].unique())
with st.sidebar.expander(LOCAL_COMPRA):
    local_compra = st.multiselect('Selecione o local da compra', dados[LOCAL_COMPRA].unique(), dados[LOCAL_COMPRA].unique())
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliação da compra',1,5, value = (1,5))
with st.sidebar.expander(TIPO_PGTO):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento',dados[TIPO_PGTO].unique(), dados[TIPO_PGTO].unique())
with st.sidebar.expander('Quantidade de parcelas'):
    qtd_parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1,24))

query = f"""
    `{PRODUTO}` in @produtos and \
    `{CATEGORIA}` in @categorias and \
    @preco[0] <= `{PRECO}` <= @preco[1] and \
    @frete[0] <= `{FRETE}` <= @frete[1] and \
    @data_compra[0] <= `{DATA_COMPRA}` <= @data_compra[1] and \
    `{VENDEDOR}` in @vendedores and \
    `{LOCAL_COMPRA}` in @local_compra and \
    @avaliacao[0] <= `{AVALIACAO}` <= @avaliacao[1] and \
    `{TIPO_PGTO}` in @tipo_pagamento and \
    @qtd_parcelas[0] <= `{QTDA_PARCELA}` <= @qtd_parcelas[1]
"""

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas')

st.download_button('Fazer o download da tabela em csv', data = converte_csv(dados_filtrados), file_name = 'dados.csv', mime = 'text/csv', on_click = mensagem_sucesso)