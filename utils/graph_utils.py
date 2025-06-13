import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from utils.database import get_all, get_count, get_mean, get_sum, get_unique

def aplicar_filtro_mensal():
    meses = get_unique("voos", "mes")
    with st.sidebar:
        mes_selecionado = st.selectbox(
            "📅 Selecione o Mês: ",
            options=[0] + (meses),
            format_func=lambda x: "Todos os Meses" if x == 0 else f"Mês {x}"
        )
    if mes_selecionado == 0:
        return {}
    return {"mes": mes_selecionado}

def mostrar_big_numbers(ft):
    st.subheader("📈 Big Numbers")

    col1, col2, col3 = st.columns(3)
    col4, col5, col6  = st.columns(3)
    col7, col8, col9 = st.columns(3)
    
    passageiros =  get_sum("voos", ["passageiros_pagos", "passageiros_gratis"], filters=ft)
    voos = get_sum("voos", ["decolagens"], filters=ft)
    combustivel = get_sum("voos", ["combustivel_litros"], filters=ft)
    
    col1.metric("👨‍👩‍👧‍👦Passageiros Totais", passageiros)
    col2.metric("🛫Decolagens Totais", voos)
    col3.metric("⏳Horas Voadas Totais", get_sum("voos", ["horas_voadas"], filters=ft))
    col4.metric("⛽Combustível Total (L)", combustivel)
    col5.metric("🗺️Distância Voada Total", get_sum("voos", ["distancia_voada_km"], filters=ft))
    col6.metric("📦Carga Total", get_sum("voos", ["carga_paga_kg", "carga_gratis_kg", "correio_kg"], filters=ft))
    col7.metric("📮Correio Total", get_sum("voos", ["correio_kg"], filters=ft))
    col8.metric("🏔️Média de Passageiros Por Voo", f"{(passageiros/voos):,.2f}")
    col9.metric("🪽Média de Combustível Por Voo", f"{(combustivel/voos):,.2f}")

def grafico_natureza_voos(ft):
    contagem = get_count("voos", group_by="natureza")
    contagem.columns = ["Tipo de Voo", "Quantidade"]

    color_map = {
        "DOMÉSTICA": "#4DA6FF",
        "INTERNACIONAL": "#003366	"
    }

    fig = px.pie(contagem, 
    names="Tipo de Voo", 
    values="Quantidade", 
    title="Distribuição de Voos por Natureza", 
    color="Tipo de Voo", 
    color_discrete_map=color_map
    )
    st.plotly_chart(fig)

# def grafico_assentos_usados(ft):
#     usados = get_sum("voos", fields=["passageiros_pagos", "passageiros_gratis"])
#     usados_columns = ["Situação", "Média de Assentos"]

#     color_map = {
#         "OCUPADOS": "green",
#         "VAGOS": "red"
#     }

#     fig = px.pie(usados,
#         names="Situação",
#         values="Média de Assentos",
#         title="Média de Ocupação de Assentos por Voo",
#         color="Situação",
#         color_discrete_map=color_map
#     )
#     st.plotly_chart(fig)

def grafico_destino_por_continente(df):
    contagem = get_count("RelatorioVoosDetalhado", group_by="continente_aeroporto_destino")
    contagem.columns = ["Continente de Destino", "Quantidade de Voos"]

    color_map = {
        "AMÉRICA DO SUL": "#000080",
        "AMÉRICA DO NORTE": "#008080",
        "EUROPA": "#D678EB",
        "ÁFRICA": "#000000",
        "ÁSIA": "#F5EA21",
        "OCEANIA": "#98F571"
    }

    fig = px.pie(contagem,
                 names="Continente de Destino",
                 values="Quantidade de Voos",
                 title="Distribuição de Voos por Continente de Destino",
                 color="Continente de Destino",
                 color_discrete_map=color_map
    )
    st.plotly_chart(fig)

# def grafico_voos_por_empresa(df, top_n= 3):
#     voos_por_empresa = df.groupby("nome_empresa")["decolagens"].sum().sort_values(ascending=False)

#     top_empresas = voos_por_empresa.head(top_n)
#     outras = voos_por_empresa.iloc[top_n:].sum()

#     dados = top_empresas.copy()
#     if outras > 0:
#         dados["Outras"] = outras

#     dados = dados.reset_index()
#     dados.columns = ["Empresa", "Decolagens"]

#     fig = px.pie(dados, names="Empresa", values="Decolagens", title=f"Top {top_n} Empresas por Número de Voos")
#     st.plotly_chart(fig)

def grafico_grupo_voo(df):
    dados = get_count("voos")
    fig = px.sunburst(dados, path=["natureza", "grupo_voo"], values="Quantidade",
    title="Distribuição por Natureza e Grupo de Voo")
    st.plotly_chart(fig)

# def grafico_empresa_nacionalidade(df):
#     dados = df["nacionalidade_empresa"].value_counts().reset_index()
#     dados.columns = ["Nacionalidade", "Quantidade"]
#     fig = px.pie(dados, names="Nacionalidade", values="Quantidade", title="Empresas por Nacionalidade")
#     st.plotly_chart(fig)

def mostrar_graficos(df):
    st.subheader("📶 Gráficos")

    col1, col2 = st.columns(2)
    with col1:
        grafico_natureza_voos(df)
    # with col2:
    #     grafico_assentos_usados(df)

    col3, col4 = st.columns(2)
    with col3:
        grafico_destino_por_continente(df)
    # with col4:
    #     grafico_voos_por_empresa(df)

    col5, col6 = st.columns(2)
    with col5:
        grafico_grupo_voo(df)
    # with col6:
    #     grafico_empresa_nacionalidade(df)  

def mostrar_comparativo_mensal_percentual():
    df_mes = get_all(table="VariacaoMensal")
    df_plot = df_mes.set_index('mes')

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