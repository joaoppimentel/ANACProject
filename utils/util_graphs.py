import pandas as pd
import plotly.express as px
import streamlit as st

def calcular_total_passageiros(df):
    return df["PASSAGEIROS PAGOS"].sum() + df["PASSAGEIROS GRÁTIS"].sum()

def calcular_total_voos(df):
    return df["DECOLAGENS"].sum()

def calcular_total_horas_voadas(df):
    return pd.to_numeric(df["HORAS VOADAS"], errors="coerce").fillna(0).sum()

def calcular_total_combustivel(df):
    return df["COMBUSTÍVEL (LITROS)"].sum()

def calcular_total_bagagem(df):
    return df["BAGAGEM (KG)"].sum()

def calcular_total_empresas(df):
    return df["EMPRESA (NOME)"].nunique()

def media_passageiro_voo(df):
    total_passageiros = calcular_total_passageiros(df)
    total_voos = calcular_total_voos(df)
    if total_voos == 0:
        return 0
    return total_passageiros / total_voos

def media_combustivel_voo(df):
    total_combustivel = calcular_total_combustivel(df)
    total_voos = calcular_total_voos(df)
    if total_voos == 0:
        return 0
    return total_combustivel / total_voos

def calcular_total_aeroportos(df):
    return df["AEROPORTO DE ORIGEM (NOME)"].nunique()

def grafico_natureza_voos(df):
    contagem = df["NATUREZA"].value_counts().reset_index()
    contagem.columns = ["Tipo de Voo", "Quantidade"]
    fig = px.pie(contagem, names="Tipo de Voo", values="Quantidade", title="Distribuição de Voos por Natureza")
    st.plotly_chart(fig)

def grafico_assentos_usados(df):
    df["ASSENTOS"] = pd.to_numeric(df["ASSENTOS"], errors="coerce").fillna(0)
    usados = df["PASSAGEIROS PAGOS"] + df["PASSAGEIROS GRÁTIS"]
    totais = df["ASSENTOS"]

    media_ocupados = usados.mean()
    media_totais = totais.mean()
    media_vagos = media_totais - media_ocupados

    dados = pd.DataFrame({
        "Situação": ["Ocupados", "Vagos"],
        "Média de Assentos": [media_ocupados, media_vagos]
    })
 
    fig = px.pie(dados, names="Situação", values="Média de Assentos", title="Média de Ocupação de Assentos por Voo")
    st.plotly_chart(fig)

def grafico_destino_por_continente(df):
    contagem = df["AEROPORTO DE DESTINO (CONTINENTE)"].value_counts().reset_index()
    contagem.columns = ["Continente de Destino", "Quantidade de Voos"]

    fig = px.pie(contagem,
                 names="Continente de Destino",
                 values="Quantidade de Voos",
                 title="Distribuição de Voos por Continente de Destino")

    st.plotly_chart(fig)

def grafico_voos_por_empresa(df, top_n= 3):
    voos_por_empresa = df.groupby("EMPRESA (NOME)")["DECOLAGENS"].sum().sort_values(ascending=False)

    top_empresas = voos_por_empresa.head(top_n)
    outras = voos_por_empresa.iloc[top_n:].sum()

    dados = top_empresas.copy()
    if outras > 0:
        dados["Outras"] = outras

    dados = dados.reset_index()
    dados.columns = ["Empresa", "Decolagens"]

    fig = px.pie(dados, names="Empresa", values="Decolagens", title=f"Top {top_n} Empresas por Número de Voos")
    st.plotly_chart(fig)

def grafico_distribuicao_passageiros(df):
    pagos = df["PASSAGEIROS PAGOS"].sum()
    gratis = df["PASSAGEIROS GRÁTIS"].sum()

    dados = pd.DataFrame({
        "Tipo de Passageiro": ["Pagos", "Grátis"],
        "Quantidade": [pagos, gratis]
    })

    fig = px.pie(dados, names="Tipo de Passageiro", values="Quantidade", title="Distribuição de Passageiros (Pagos vs Grátis)")
    st.plotly_chart(fig)