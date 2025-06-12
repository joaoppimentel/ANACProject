import streamlit as st
from utils.graph_utils import mostrar_big_numbers, mostrar_graficos, aplicar_filtro_mensal, mostrar_comparativo_mensal_percentual

st.title("📈 Big Numbers e Gráficos ANAC 📊")

df = aplicar_filtro_mensal()
st.dataframe(df)
mostrar_big_numbers(df)
mostrar_comparativo_mensal_percentual(df)
mostrar_graficos(df)