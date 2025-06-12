import streamlit as st
from unidecode import unidecode
from utils.database import execute_query, format_filters, get_types

def raw_tables():
    filters = sidebar_filters()

    st.header("Tabela Aeroportos")
    query = "SELECT * FROM aeroportos"
    if filters['aero']:
        query += " WHERE "+ format_filters(filters["aero"])
    df = execute_query(query, df=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.subheader("Aeroportos Encontrados: "+str(len(df)))
    st.divider()

    st.header("Tabela Empresas")
    query = "SELECT * FROM empresas"
    if filters['emp']:
        query += " WHERE "+ format_filters(filters["emp"])
    df = execute_query(query, df=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.subheader("Empresas Encontradas: "+str(len(df)))
    st.divider()

    st.header("Tabela Completa")
    query = "SELECT * FROM RelatorioVoosDetalhado"
    voos_filter = []
    if filters["aero"]:
        origem_ft = format_filters(filters["aero"], suffix="_aeroporto_origem")
        destino_ft = format_filters(filters["aero"], suffix="_aeroporto_destino")
        voos_filter.append(f"({origem_ft} OR {destino_ft})")

    if filters["emp"]:
        voos_filter.append(format_filters(filters["emp"], suffix="_empresa"))

    if filters['voos']:
        voos_filter.append(format_filters(filters["voos"]))
            
    if voos_filter:
        query += " WHERE "+ " AND ".join(voos_filter)
    df = execute_query(query, df=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.subheader("Voos Encontrados: "+str(len(df)))
    st.divider()

def sidebar_filters():
    with st.sidebar:
        filtros = {}
        st.header("Filtros")
        filtros['aero'] = filter_container(
            name="Aeroporto",
            labels=["Sigla", "Nome", "UF", "Região", "País", "Continente"],
            table='aeroportos'
        )

        filtros['emp'] = filter_container(
            name="Empresas",
            labels=["Sigla", "Nome", "Nacionalidade"],
            table='empresas'
        )

        filtros['voos'] = filter_container(
            name="Voos",
            labels=["Ano", "Mês", "Natureza", "Grupo Voo"],
            table='voos'
        )
    return filtros

def filter_container(name, labels, table):
    df = execute_query(f"SELECT * FROM {table}", df=True)
    filters = {}
    prefix = clean_name(name)
    with st.expander(name):
            if st.button("Resetar filtros", key=f'reset_{prefix}'):
                for l in labels:
                    low_name = clean_name(l)
                    key = f"{prefix}_{low_name}"
                    st.session_state[key] = None

            for l in labels:
                low_name = clean_name(l)
                tmp_ft = selectbox(l, df, prefix)
                types = get_types(table)
                if tmp_ft:
                   if types[low_name] == "INTEGER":
                    filters[low_name] = tmp_ft
                   else:
                    filters[low_name] = tmp_ft
    return filters


def selectbox(label, df, key_prefix, column=''):
    key = clean_name(label)
    if not column:
        column = key
    key = f"{key_prefix}_{key}"
    options = df[column].dropna().sort_values().unique()
    return st.selectbox(label, options, key=key, index=None)

def clean_name(name):
    name = unidecode(name.lower())
    name = name.strip().replace(" ", "_")
    return name

