import streamlit as st
import dados
import pandas as pd

st.title('Filmes')

nome = st.text_input('Nome do filme:')
ano = st.number_input('Ano do filme:', min_value=2010, max_value=2025)
nota = st.slider("Nota do filme", min_value=0, max_value=10)

if st.button('Adicionar'):
    dados.insere_dados(nome,ano,nota)
    st.success('Filme cadastrado')
    
filmes = dados.obter_dados()
st.header('Lista de filmes')

df_filmes = pd.DataFrame(filmes, columns=['Id', 'Título', 'Ano', 'Nota'])

# Exibir a tabela interativa usando st.dataframe()
st.subheader("Tabela Interativa (st.dataframe)")
st.dataframe(df_filmes)