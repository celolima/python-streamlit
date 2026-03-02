import pandas as pd
import plotly.express as px

def build_receita_vendedores(dados,qtd):
    vendedores = build_dataframe_agrega_vendedor(dados)
    
    fig_receita_vendedores = px.bar(
        vendedores[['sum']].sort_values('sum', ascending=False).head(qtd),
        x='sum',
        y=vendedores[['sum']].sort_values('sum', ascending=False).head(qtd).index,
        text_auto=True,
        title=f'Top {qtd} vendedores (receita)',
        labels={"sum": "Receita total", "y": "Vendedor"}
    )
    return fig_receita_vendedores

def build_qtde_vendedores(dados,qtd):
    vendedores = build_dataframe_agrega_vendedor(dados)
    
    fig_vendas_vendedores = px.bar(
        vendedores[['count']].sort_values('count', ascending=False).head(qtd),
        x='count',
        y=vendedores[['count']].sort_values('count', ascending=False).head(qtd).index,
        text_auto=True,
        title=f'Top {qtd} vendedores (quantidade de vendas)',
        labels={"count": "Quantidade total", "y": "Vendedor"}
    )
    return fig_vendas_vendedores

def build_dataframe_agrega_vendedor(dados):
    return pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum', 'count']))