import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from babel.numbers import format_currency, format_decimal

st.title('DASHBOARD DE VENDAS :shopping_cart:')

url = 'https://labdados.com/produtos'
response = requests.get(url, verify=False)
dados = pd.DataFrame.from_dict(response.json())

## Tabelas
LOCAL_COMPRA = 'Local da compra'
tb_receita_estados = dados.groupby(LOCAL_COMPRA)[['Preço']].sum()
tb_estados_locale = dados.drop_duplicates(subset=LOCAL_COMPRA)[[LOCAL_COMPRA, 'lat', 'lon']]

# Faz o join das tabelas acima, a tabela da esquerda usa index e a da direita usa a coluna Local da compra
tb_merge_tabelas = tb_receita_estados.merge(tb_estados_locale, left_index=True, right_on=LOCAL_COMPRA).sort_values('Preço', ascending=False)

## Gráficos
# Altera o tamanho do ponto baseado na receita
fig_mapa_receita = px.scatter_geo(
                                    tb_merge_tabelas,
                                    lat='lat',
                                    lon='lon',
                                    scope='south america',
                                    size='Preço',
                                    template='seaborn',
                                    hover_name=LOCAL_COMPRA,
                                    hover_data={'lat': False, 'lon': False},
                                    title='Receita por estado'
                                )

## Visualização no streamlit
coluna1, coluna2 = st.columns(2)
with coluna1:
    total_preco = dados['Preço'].sum()
    st.metric('Receita', format_currency(total_preco, 'BRL', locale='pt_BR'))
    st.plotly_chart(fig_mapa_receita)
with coluna2:
    st.metric('Quantidade de vendas', format_decimal(dados.shape[0], locale='pt_BR'))

st.dataframe(dados)