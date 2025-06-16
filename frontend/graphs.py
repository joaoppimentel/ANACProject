import streamlit as st
from utils.flies_map import render_map
from utils.graph_utils import mostrar_big_numbers, mostrar_graficos, aplicar_filtro_mensal, mostrar_comparativo_mensal_percentual
from utils.database import get_all

big_numbers, graphs, flies_map = st.tabs(["Big Numbers", "Gráficos", "Mapa de Voos"])


df = get_all("RelatorioVoosDetalhado")
df, ft = aplicar_filtro_mensal(df)
with big_numbers:
    mostrar_big_numbers(df)
with graphs:
    st.title("📈 Gráficos ANAC 📊")
    if not ft != 0:
        mostrar_comparativo_mensal_percentual(df)
    mostrar_graficos(df)
with flies_map:
    st.title("🛬 Mapa das rotas de Voo 🗺")
    render_map(ft)