import streamlit as st
from utils.graph_utils import mostrar_big_numbers, mostrar_graficos, aplicar_filtro_mensal, mostrar_comparativo_mensal_percentual

st.title("Big Numbers e Gráficos ANAC 📊")

ft = aplicar_filtro_mensal()
mostrar_big_numbers(ft)
if not ft:
    mostrar_comparativo_mensal_percentual()
mostrar_graficos(ft)