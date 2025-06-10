import streamlit as st
import pandas as pd
from utils.database import rename_columns, execute_query

st.title("Tabela ANAC ✈️")

df = execute_query("SELECT * FROM RelatorioVoosDetalhado", return_columns=True, fetch=True)
st.dataframe(df)