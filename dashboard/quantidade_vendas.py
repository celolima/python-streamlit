import pandas as pd
import plotly.express as px
from babel.numbers import format_currency, format_decimal

## Desafio
# 1- Construir um gráfico de mapa com a quantidade de vendas por estado.
# 2- Construir um gráfico de linhas com a quantidade de vendas mensal.
# 3- Construir um gráfico de barras com os 5 estados com maior quantidade de vendas.
# 4- Construir um gráfico de barras com a quantidade de vendas por categoria de produto.

LOCAL_COMPRA = 'Local da compra'
DATA_COMPRA = 'Data da Compra'
CATEGORIA_PRODUTO = 'Categoria do Produto'
PRECO = 'Preço'
QUANTIDADE = 'Quantidade'
ANO = 'Ano'
MES = 'Mes'

def build_grafico_mapa(dados):
    ## Tabelas
    tb_quantidade_vendas_estados = dados.groupby(LOCAL_COMPRA)[[PRECO]].count()
    tb_estados_locale = dados.drop_duplicates(subset=LOCAL_COMPRA)[[LOCAL_COMPRA, 'lat', 'lon']]
    
    # Faz o join das tabelas acima, a tabela da esquerda usa index e a da direita usa a coluna Local da compra
    tb_merge_tabelas = tb_quantidade_vendas_estados.merge(tb_estados_locale, left_index=True, right_on=LOCAL_COMPRA).sort_values(PRECO, ascending=False)
    
    print(tb_merge_tabelas.columns)
    
    print(type(tb_merge_tabelas))

    # Para aplicar diretamente no DataFrame original sem precisar atribuir à variável:
    tb_merge_tabelas.rename(columns={PRECO: QUANTIDADE}, inplace=True)
    
    print(tb_merge_tabelas.columns)

    # Altera o tamanho do ponto baseado na receita
    fig_map_quantidade_estado = px.scatter_geo(
                                    tb_merge_tabelas,
                                    lat='lat',
                                    lon='lon',
                                    scope='south america',
                                    size=QUANTIDADE,
                                    template='seaborn',
                                    hover_name=LOCAL_COMPRA,
                                    hover_data={'lat': False, 'lon': False},
                                    title='Quantidade por estado',
                                )
    return fig_map_quantidade_estado

def build_grafico_linhas(dados):
    vendas_mensal = dados.set_index(DATA_COMPRA).groupby(pd.Grouper(freq='ME'))[PRECO].count().reset_index()
    vendas_mensal[ANO] = vendas_mensal[DATA_COMPRA].dt.year
    vendas_mensal[MES] = vendas_mensal[DATA_COMPRA].dt.month_name()

    vendas_mensal.rename(columns={PRECO: QUANTIDADE}, inplace=True)    

    fig_vendas_mensal = px.line(
                            vendas_mensal,
                            x=MES,
                            y=QUANTIDADE,
                            markers=True,
                            range_y=(0,vendas_mensal.max()),
                            color=ANO,
                            line_dash=ANO,
                            title='Receita Mensal'
                        )

    fig_vendas_mensal.update_layout(yaxis_title='Quantidade')

    return fig_vendas_mensal

def build_grafico_barras(dados,group_by=LOCAL_COMPRA):
    df_agrupado = dados.groupby(group_by, as_index=False)[PRECO].count().sort_values(PRECO, ascending=False)
    df_agrupado["Quantidade_formatada"] = df_agrupado[PRECO].apply(lambda x: format_decimal(x, locale="pt_BR"))

    title = 'Top 5 estados (quantidade vendas)' if group_by==LOCAL_COMPRA else f'Quantidade de vendas {group_by}'
    
    df_agrupado.rename(columns={PRECO: QUANTIDADE}, inplace=True)
    
    fig_quantidade_vendas = px.bar(
        df_agrupado.head() if group_by==LOCAL_COMPRA else df_agrupado,
        x=group_by,
        y=QUANTIDADE,
        text=df_agrupado["Quantidade_formatada"].head() if group_by==LOCAL_COMPRA else df_agrupado["Quantidade_formatada"],
        title=title
    )
    fig_quantidade_vendas.update_layout(yaxis_title='Quantidade')
    return fig_quantidade_vendas