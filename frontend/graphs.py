import streamlit as st
import pandas as pd
from utils.util_graphs import carregar_dados, mostrar_big_numbers, mostrar_graficos, aplicar_filtro_mensal, mostrar_comparativo_mensal_percentual
from utils.database import rename_columns, execute_query

st.title("📈 Big Numbers e Gráficos ANAC 📊")

df = carregar_dados()
df, mes_selecionado = aplicar_filtro_mensal(df)
st.dataframe(df)
mostrar_comparativo_mensal_percentual(df)
mostrar_big_numbers(df)
mostrar_graficos(df)