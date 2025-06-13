import streamlit as st
from utils.flies_map import render_map
from utils.graph_utils import mostrar_big_numbers, mostrar_graficos, aplicar_filtro_mensal, mostrar_comparativo_mensal_percentual

big_numbers, graphs, flies_map = st.tabs(["Big Numbers", "Gráficos", "Mapa de Voos"])

ft = aplicar_filtro_mensal()
with big_numbers:
    st.title("📈 Big Numbers📊")

    mostrar_big_numbers(ft)
with graphs:
    st.title("📈 Gráficos ANAC 📊")
    if not ft:
      mostrar_comparativo_mensal_percentual()
    mostrar_graficos(ft)

with flies_map:
    st.title("🗺️Mapa Voos🛫")

    # render_map()
