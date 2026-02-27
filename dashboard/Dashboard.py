import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from babel.numbers import format_currency, format_decimal

# Nomes das colunas
LOCAL_COMPRA = 'Local da compra'
DATA_COMPRA = 'Data da Compra'
PRECO = 'Preço'
ANO = 'Ano'
MES = 'Mes'

st.title('DASHBOARD DE VENDAS :shopping_cart:')
st.set_page_config(layout='wide')

url = 'https://labdados.com/produtos'
response = requests.get(url, verify=False)
dados = pd.DataFrame.from_dict(response.json())
dados[DATA_COMPRA] = pd.to_datetime(dados[DATA_COMPRA], format='%d/%m/%Y')

## Tabelas
tb_receita_estados = dados.groupby(LOCAL_COMPRA)[[PRECO]].sum()
tb_estados_locale = dados.drop_duplicates(subset=LOCAL_COMPRA)[[LOCAL_COMPRA, 'lat', 'lon']]

receita_mensal = dados.set_index(DATA_COMPRA).groupby(pd.Grouper(freq='M'))[PRECO].sum().reset_index()
receita_mensal[ANO] = receita_mensal[DATA_COMPRA].dt.year
receita_mensal[MES] = receita_mensal[DATA_COMPRA].dt.month_name()

# Faz o join das tabelas acima, a tabela da esquerda usa index e a da direita usa a coluna Local da compra
tb_merge_tabelas = tb_receita_estados.merge(tb_estados_locale, left_index=True, right_on=LOCAL_COMPRA).sort_values(PRECO, ascending=False)

## Gráficos
# Altera o tamanho do ponto baseado na receita
fig_mapa_receita = px.scatter_geo(
                                    tb_merge_tabelas,
                                    lat='lat',
                                    lon='lon',
                                    scope='south america',
                                    size=PRECO,
                                    template='seaborn',
                                    hover_name=LOCAL_COMPRA,
                                    hover_data={'lat': False, 'lon': False},
                                    title='Receita por estado'
                                )

fig_receita_mensal = px.line(   
                                receita_mensal,
                                x=MES,
                                y=PRECO,
                                markers=True,
                                range_y=(0,receita_mensal.max()),
                                color=ANO,
                                line_dash=ANO,
                                title='Receita Mensal'
                            )

fig_receita_mensal.update_layout(yaxis_title='Receita')

## Visualização no streamlit
coluna1, coluna2 = st.columns(2)
with coluna1:
    total_preco = dados[PRECO].sum()
    st.metric('Receita', format_currency(total_preco, 'BRL', locale='pt_BR'))
    st.plotly_chart(fig_mapa_receita, use_container_width=True)
with coluna2:
    st.metric('Quantidade de vendas', format_decimal(dados.shape[0], locale='pt_BR'))
    st.plotly_chart(fig_receita_mensal, use_container_width=True)
    
st.dataframe(
    dados,
    column_config={
        DATA_COMPRA: st.column_config.DateColumn(
            "Data de Compra",
            format="DD/MM/YYYY",  # Formato de exibição visual
        )
    }
)