import streamlit as st
import pandas as pd
from utils.database import create_tables, fill_tables, create_views

def main():
    st.set_page_config(page_title="ANAC", layout="wide")
    df = pd.read_csv('./data/anac.csv', encoding='latin-1', delimiter=";")
    create_tables()
    fill_tables(df)
    create_views()

    tables = st.Page("./frontend/tables.py", title="Tabela ANAC", icon="✈️", default=True)
    graphs = st.Page("./frontend/graphs.py", title="Gráficos ANAC", icon="📈")

    pg = st.navigation([tables, graphs])
    pg.run()


if __name__ == "__main__":
    main()