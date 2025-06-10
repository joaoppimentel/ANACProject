import streamlit as st
import pandas as pd
import plotly.express as px

from frontend.graphs import mostrar_big_numbers, mostrar_graficos
from utils.database import create_tables

def carregar_dados():
    df = pd.read_csv('./data/anac.csv', encoding='latin-1', delimiter=';')

    cols_to_numeric = [
        "PASSAGEIROS PAGOS",
        "PASSAGEIROS GRÁTIS",
        "DECOLAGENS",
        "HORAS VOADAS",
        "COMBUSTÍVEL (LITROS)",
        "BAGAGEM (KG)",
        "ASSENTOS"
    ]
    for col in cols_to_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

for col in cols_to_numeric:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
st.title("Tabela ANAC ✈️")

df = pd.read_csv('./data/anac.csv', encoding='latin-1', delimiter=";")
df

cols_to_numeric = [
    "PASSAGEIROS PAGOS",
    "PASSAGEIROS GRÁTIS",
    "DECOLAGENS",
    "HORAS VOADAS",
    "COMBUSTÍVEL (LITROS)",
    "BAGAGEM (KG)"
]

from utils.util_graphs import (
    calcular_total_bagagem,
    calcular_total_combustivel,
    calcular_total_empresas,
    calcular_total_horas_voadas,
    calcular_total_passageiros,
    calcular_total_voos,
    media_combustivel_voo,
    media_passageiro_voo,
    calcular_total_aeroportos
)

def mostrar_big_numbers(df):
    st.subheader("📈 Big Numbers")

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)

    col1.metric("👨‍👩‍👧‍👦Passageiros Totais", f"{calcular_total_passageiros(df):,}")
    col2.metric("🛫Decolagens Totais", f"{calcular_total_voos(df):,}")
    col3.metric("⏳Horas Voadas Totais", f"{calcular_total_horas_voadas(df):,.2f}")
    col4.metric("⛽Combustível Total (L)", f"{calcular_total_combustivel(df):,}")
    col5.metric("🧳Bagagens Totais (KG)", f"{calcular_total_bagagem(df):,}")
    col6.metric("🗃️Empresas Ativas", f"{calcular_total_empresas(df):,}")
    col7.metric("🏔️Média de Passageiros Por Voo", f"{media_passageiro_voo(df):,.2f}")
    col8.metric("🪽Média de Combustível Por Voo", f"{media_combustivel_voo(df):,.2f}")
    col9.metric("🚡Aeroportos Atendidos", f"{calcular_total_aeroportos(df):,}")

from utils.util_graphs import (
    grafico_assentos_usados,
    grafico_destino_por_continente,
    grafico_natureza_voos,
    grafico_distribuicao_passageiros,
    grafico_voos_por_empresa
)

def mostrar_graficos(df):
    st.subheader("📶Gráficos")

    grafico_assentos_usados(df)
    grafico_destino_por_continente(df)
    grafico_natureza_voos(df)
    grafico_distribuicao_passageiros(df)
    grafico_voos_por_empresa(df)