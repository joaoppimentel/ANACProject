import streamlit as st
from utils.table_utils import raw_tables

st.title("Tabelas ANAC ✈️")
st.divider()

raw_tables()
