import streamlit as st
import pandas as pd

path_compras = "datasets/compras.csv"

df_compras = pd.read_csv(path_compras,decimal=",",sep=";")

st.dataframe(df_compras)