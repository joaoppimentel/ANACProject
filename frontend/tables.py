import streamlit as st
from utils.database import format_filters
from utils.table_utils import render_tables

st.title("Tabelas ANAC ✈️")
st.divider()

render_tables()