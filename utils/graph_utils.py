import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from utils.database import get_all

def aplicar_filtro_mensal():
    df = get_all("RelatorioVoosDetalhado")
    meses_disponiveis = sorted(df["mes"].unique())
    with st.sidebar:
        mes_selecionado = st.selectbox(
            "📅 Selecione o Mês: ",
            options=[0] + list(meses_disponiveis),
            format_func=lambda x: "Todos os Meses" if x == 0 else f"Mês {x}"
        )
    if mes_selecionado != 0:
        df = df[df["mes"] == mes_selecionado]
    return df

def calcular_total_passageiros(df):
    return df["passageiros_pagos"].sum() + df["passageiros_gratis"].sum()

def calcular_total_voos(df):
    return df["decolagens"].sum()

def calcular_total_horas_voadas(df):
    return pd.to_numeric(df["horas_voadas"], errors="coerce").fillna(0).sum()

def calcular_total_combustivel(df):
    return df["combustivel_litros"].sum()

def calcular_total_bagagem(df):
    return df["bagagem_kg"].sum()

def calcular_total_empresas(df):
    return df["nome_empresa"].nunique()

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
    return df["nome_aeroporto_origem"].nunique()

def  calcular_total_distancia(df):
    return df["distancia_voada_km"].sum()

def calcular_carga_total(df):
    return (df["carga_paga_kg"] + df["carga_gratis_kg"] + df["correio_kg"]).sum()

def calcular_correio_total(df):
    return df["correio_kg"].sum()

def grafico_natureza_voos(df):
    contagem = df["natureza"].value_counts().reset_index()
    contagem.columns = ["Tipo de Voo", "Quantidade"]
    fig = px.pie(contagem, names="Tipo de Voo", values="Quantidade", title="Distribuição de Voos por Natureza")
    st.plotly_chart(fig)

def grafico_assentos_usados(df):
    df["assentos"] = pd.to_numeric(df["assentos"], errors="coerce").fillna(0)
    usados = df["passageiros_pagos"] + df["passageiros_gratis"]
    totais = df["assentos"]

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
    contagem = df["continente_aeroporto_destino"].value_counts().reset_index()
    contagem.columns = ["Continente de Destino", "Quantidade de Voos"]

    fig = px.pie(contagem,
                 names="Continente de Destino",
                 values="Quantidade de Voos",
                 title="Distribuição de Voos por Continente de Destino")

    st.plotly_chart(fig)

def grafico_voos_por_empresa(df, top_n= 3):
    voos_por_empresa = df.groupby("nome_empresa")["decolagens"].sum().sort_values(ascending=False)

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
    pagos = df["passageiros_pagos"].sum()
    gratis = df["passageiros_gratis"].sum()

    dados = pd.DataFrame({
        "Tipo de Passageiro": ["Pagos", "Grátis"],
        "Quantidade": [pagos, gratis]
    })

    fig = px.pie(dados, names="Tipo de Passageiro", values="Quantidade", title="Distribuição de Passageiros (Pagos vs Grátis)")
    st.plotly_chart(fig)

def grafico_grupo_voo(df):
    dados = df.groupby(["natureza", "grupo_voo"]).size().reset_index(name="Quantidade")
    fig = px.sunburst(dados, path=["natureza", "grupo_voo"], values="Quantidade",
    title="Distribuição por Natureza e Grupo de Voo")
    st.plotly_chart(fig)

def grafico_valor_carga(df):
    dados = pd.DataFrame({
    "Tipo de Carga": ["Paga", "Grátis"],
    "Quantidade": [df["carga_paga_kg"].sum(), df["carga_gratis_kg"].sum()]
})
    fig = px.pie(dados, names="Tipo de Carga", values="Quantidade", title="Distribuição da Carga Transportada")
    st.plotly_chart(fig)

def grafico_empresa_nacionalidade(df):
    dados = df["nacionalidade_empresa"].value_counts().reset_index()
    dados.columns = ["Nacionalidade", "Quantidade"]
    fig = px.pie(dados, names="Nacionalidade", values="Quantidade", title="Empresas por Nacionalidade")
    st.plotly_chart(fig)

def mostrar_big_numbers(df):
    st.subheader("📈 Big Numbers")

    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7, col8 = st.columns(4)
    col9, col10, col11, col12 = st.columns(4)

    col1.metric("👨‍👩‍👧‍👦Passageiros Totais", f"{calcular_total_passageiros(df):,}")
    col2.metric("🛫Decolagens Totais", f"{calcular_total_voos(df):,}")
    col3.metric("⏳Horas Voadas Totais", f"{calcular_total_horas_voadas(df):,.2f}")
    col4.metric("⛽Combustível Total (L)", f"{calcular_total_combustivel(df):,}")
    col5.metric("🧳Bagagens Totais (KG)", f"{calcular_total_bagagem(df):,}")
    col6.metric("🗃️Empresas Ativas", f"{calcular_total_empresas(df):,}")
    col7.metric("🏔️Média de Passageiros Por Voo", f"{media_passageiro_voo(df):,.2f}")
    col8.metric("🪽Média de Combustível Por Voo", f"{media_combustivel_voo(df):,.2f}")
    col9.metric("🚡Aeroportos Atendidos", f"{calcular_total_aeroportos(df):,}")
    col10.metric("🗺️Distância Voada Total", f"{calcular_total_distancia(df):,}")
    col11.metric("📦Carga Total", f"{calcular_carga_total(df):,}")
    col12.metric("📮Correio Total", f"{calcular_correio_total(df):,}")

def mostrar_graficos(df):
    st.subheader("📶 Gráficos")

    col1, col2 = st.columns(2)
    with col1:
        grafico_assentos_usados(df)
    with col2:
        grafico_destino_por_continente(df)

    col3, col4 = st.columns(2)
    with col3:
        grafico_natureza_voos(df)
    with col4:
        grafico_distribuicao_passageiros(df)

    col5, col6 = st.columns(2)
    with col5:
        grafico_voos_por_empresa(df)
    with col6:
        grafico_grupo_voo(df)  

    col7, col8 = st.columns(2)
    with col7:
        grafico_valor_carga(df)  
    with col8:
        grafico_empresa_nacionalidade(df)  

def mostrar_comparativo_mensal_percentual(df):
    meses_disponiveis = sorted(df['mes'].unique())
    df = df[df["mes"].isin(meses_disponiveis)]

    df_mes = df.groupby('mes').agg({
        "passageiros_pagos": "sum",
        "decolagens": "sum",
        "combustivel_litros": "sum",
        "carga_paga_kg": "sum"
    }).reset_index()

    df_mes = df_mes.sort_values('mes')
    df_plot = df_mes.set_index('mes')
    df_plot = df_plot.rename(columns={
        "passageiros_pagos": "Passageiros",
        "decolagens": "Voos",
        "combustivel_litros": "Combustível (L)",
        "carga_paga_kg": "Carga (Kg)"
    })

    scaler = MinMaxScaler()
    df_normalizado = pd.DataFrame(
        scaler.fit_transform(df_plot),
        columns=df_plot.columns,
        index=df_plot.index
    )

    df_pct = df_plot.pct_change().fillna(0) * 100

    st.subheader("↘️ Variação Mensal ↗️")
    st.line_chart(df_normalizado)

    st.subheader("🔁 Variação Percentual Mensal")
    st.dataframe(
        df_pct.style.format("{:.2f}%")
        .highlight_max(axis=0, color='lightgreen')
        .highlight_min(axis=0, color='lightcoral'),
        use_container_width=True
    )