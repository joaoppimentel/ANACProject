import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import MinMaxScaler

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

def  calcular_total_distancia(df):
    return df["DISTÂNCIA VOADA (KM)"].sum()

def calcular_carga_total(df):
    return (df["CARGA PAGA (KG)"] + df["CARGA GRÁTIS (KG)"] + df["CORREIO (KG)"]).sum()

def calcular_correio_total(df):
    return df["CORREIO (KG)"].sum()

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

def grafico_grupo_voo(df):
    dados = df.groupby(["NATUREZA", "GRUPO DE VOO"]).size().reset_index(name="Quantidade")
    fig = px.sunburst(dados, path=["NATUREZA", "GRUPO DE VOO"], values="Quantidade",
    title="Distribuição por Natureza e Grupo de Voo")
    st.plotly_chart(fig)

def grafico_valor_carga(df):
    dados = pd.DataFrame({
    "Tipo de Carga": ["Paga", "Grátis"],
    "Quantidade": [df["CARGA PAGA (KG)"].sum(), df["CARGA GRÁTIS (KG)"].sum()]
})
    fig = px.pie(dados, names="Tipo de Carga", values="Quantidade", title="Distribuição da Carga Transportada")
    st.plotly_chart(fig)

def grafico_empresa_nacionalidade(df):
    dados = df["EMPRESA (NACIONALIDADE)"].value_counts().reset_index()
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

import streamlit as st

def aplicar_filtro_mensal(df):
    meses_disponiveis = sorted(df["MÊS"].unique())
    mes_selecionado = st.selectbox(
        "📅 Selecione o Mês: ",
        options=[0] + list(meses_disponiveis),
        format_func=lambda x: "Todos os Meses" if x == 0 else f"Mês {x}"
    )
    if mes_selecionado != 0:
        df = df[df["MÊS"] == mes_selecionado]
    return df, mes_selecionado


def mostrar_comparativo_mensal_percentual(df):
    import pandas as pd
    import streamlit as st
    from sklearn.preprocessing import MinMaxScaler

    meses_disponiveis = sorted(df['MÊS'].unique())
    df = df[df["MÊS"].isin(meses_disponiveis)]

    df_mes = df.groupby('MÊS').agg({
        "PASSAGEIROS PAGOS": "sum",
        "DECOLAGENS": "sum",
        "COMBUSTÍVEL (LITROS)": "sum",
        "CARGA PAGA (KG)": "sum"
    }).reset_index()

    df_mes = df_mes.sort_values('MÊS')
    df_plot = df_mes.set_index('MÊS')
    df_plot = df_plot.rename(columns={
        "PASSAGEIROS PAGOS": "Passageiros",
        "DECOLAGENS": "Voos",
        "COMBUSTÍVEL (LITROS)": "Combustível (L)",
        "CARGA PAGA (KG)": "Carga (Kg)"
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
        .highlight_min(axis=0, color='lightcoral')
    )