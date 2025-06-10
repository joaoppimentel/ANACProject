import streamlit as st
from utils.database import create_tables, fill_tables

def main():
    st.set_page_config(page_title="ANAC", layout="wide")

    create_tables()
    # fill_tables()

    tables = st.Page("./frontend/tables.py", title="Tabela ANAC", icon="✈️", default=True)
    graphs = st.Page("./frontend/graphs.py", title="Gráficos ANAC", icon="📈")

    pg = st.navigation([tables, graphs])
    pg.run()


if __name__ == "__main__":
    main()