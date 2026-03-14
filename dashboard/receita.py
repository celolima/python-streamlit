import pandas as pd
import plotly.express as px
from constants import *
from babel.numbers import format_currency, format_decimal

def build_grafico_mapa(dados):
    ## Tabelas
    tb_receita_estados = dados.groupby(LOCAL_COMPRA)[[PRECO]].sum()
    tb_estados_locale = dados.drop_duplicates(subset=LOCAL_COMPRA)[[LOCAL_COMPRA, 'lat', 'lon']]

    # Faz o join das tabelas acima, a tabela da esquerda usa index e a da direita usa a coluna Local da compra
    tb_merge_tabelas = tb_receita_estados.merge(tb_estados_locale, left_index=True, right_on=LOCAL_COMPRA).sort_values(PRECO, ascending=False)

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
    return fig_mapa_receita

def build_grafico_linhas(dados):
    receita_mensal = dados.set_index(DATA_COMPRA).groupby(pd.Grouper(freq='ME'))[PRECO].sum().reset_index()
    receita_mensal[ANO] = receita_mensal[DATA_COMPRA].dt.year
    receita_mensal[MES] = receita_mensal[DATA_COMPRA].dt.month_name()

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

    return fig_receita_mensal

def build_grafico_barras(dados,group_by=LOCAL_COMPRA):
    df_agrupado = dados.groupby(group_by, as_index=False)[PRECO].sum().sort_values(PRECO, ascending=False)
    df_agrupado["Preço_formatado"] = df_agrupado["Preço"].apply(lambda x: format_currency(x, "BRL", locale="pt_BR"))

    title = 'Top 5 estados (receita)' if group_by==LOCAL_COMPRA else f'Somatório de Preço por {group_by}'
    
    fig_receita = px.bar(
        df_agrupado.head() if group_by==LOCAL_COMPRA else df_agrupado,
        x=group_by,
        y=PRECO,
        text=df_agrupado["Preço_formatado"].head() if group_by==LOCAL_COMPRA else df_agrupado["Preço_formatado"],
        title=title
    )
    fig_receita.update_layout(yaxis_title='Receita')
    return fig_receita