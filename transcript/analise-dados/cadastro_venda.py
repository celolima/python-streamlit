from datetime import datetime
import streamlit as st
import pandas as pd

path_datasets = "datasets"

df_compras = pd.read_csv(f'{path_datasets}/compras.csv', sep=';', decimal=',', index_col=0)
df_lojas = pd.read_csv(f'{path_datasets}/lojas.csv', sep=';', decimal=',', index_col=0)
df_produtos = pd.read_csv(f'{path_datasets}/produtos.csv', sep=';', decimal=',')

df_lojas['cidade/estado'] = df_lojas['cidade'] + '/' + df_lojas['estado']
lista_lojas = df_lojas['cidade/estado'].to_list()
loja_selecionada = st.sidebar.selectbox('Selecione a loja: ', lista_lojas)

lista_vendedores = df_lojas.loc[df_lojas['cidade/estado'] == loja_selecionada, "vendedores"].iloc[0]
lista_vendedores = lista_vendedores.strip('][').replace("'",'').split(', ')
vendedor_selecionado = st.sidebar.selectbox('Selecione o vendedor:', lista_vendedores)

list_produtos = df_produtos['nome'].to_list()
produto_selecionado = st.sidebar.selectbox('Selecione o produto:', list_produtos)

nome_cliente = st.sidebar.text_input("Nome do cliente:")
genero_selecionado = st.sidebar.selectbox('Gênero do cliente', ['feminino','masculino'])

forma_pgto_selecionado = st.sidebar.selectbox('Forma de pagamento', ['cartão de crédito', 'cartão de débito', 'pix', 'dinheiro'])

st_add = st.sidebar.button('Adicionar')

if st_add:
    elemento = [ df_compras['id_compra'].max() + 1 if not df_compras.empty else 1,
                       loja_selecionada,
                       vendedor_selecionado,
                       produto_selecionado,
                       nome_cliente,
                       genero_selecionado,
                       forma_pgto_selecionado
                    ]
    df_compras.loc[datetime.now()] = elemento

    df_compras.to_csv(f'{path_datasets}/compras.csv', index=False, decimal=',', sep=';')
    st.success('Compra adicionada')

    st.dataframe(df_compras)