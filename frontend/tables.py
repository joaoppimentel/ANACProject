import streamlit as st
import pandas as pd
from utils.database import execute_query
from utils.table_utils import prepare_dataframe

st.title("Tabelas ANAC ✈️")
st.divider()

st.header("Tabela Detalhada")
df = execute_query("SELECT * FROM RelatorioVoosDetalhado", return_columns=True, fetch=True)
df = prepare_dataframe(df)
st.write(df)
st.divider()

st.header("Tabela Aeroportos")
df = execute_query("SELECT * FROM aeroportos", return_columns=True, fetch=True)
st.dataframe(df)
st.divider()
