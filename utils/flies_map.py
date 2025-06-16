import streamlit as st
import pydeck as pdk
import airportsdata as ad

from utils.database import get_all, get_unique

airports = ad.load()

def get_airport_cord(icao):
    try:
        airport = airports[icao]
        return [airport['lon'], airport['lat']]
    except:
        return None
    
{'mes':1}

def render_map(ft):
    filters = map_filter()
    if ft:
        filters['mes'] = int(ft)
    flies = get_all("RotasVoo",df=True, filters=filters)

    flies['cord_origem'] = flies['sigla_origem'].apply(get_airport_cord)
    flies['cord_destino'] = flies['sigla_destino'].apply(get_airport_cord)

    layer = pdk.Layer(
        "ArcLayer",
        flies,
        pickable=True,
        get_stroke_width=12,
        get_source_position="cord_origem",
        get_target_position="cord_destino",
        get_source_color=[64, 255, 0],
        get_target_color=[0, 128, 200],
        auto_highlight=True,
    )

    view_state = pdk.ViewState(latitude=50, longitude=-40, zoom=0.75, bearing=0, pitch=0)

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{nome_origem} to {nome_destino}"},
    )

    r.picking_radius = 10

    st.pydeck_chart(r)

def map_filter():
    st.header("Filtros")
    filters = {}
    with st.container(border=True):
        st.subheader("Origem")
        c1, c2 = st.columns(2)

    continentes = get_unique("RotasVoo", 'continente_origem')
    continente_origem = ""
    pais_origem = ""
    continente_destino = ""
    pais_destino = ""

    with c1:
        continente_origem = st.selectbox("Continente", continentes, index=None, key='continente_origem')
        if continente_origem:
            filters['continente_origem'] = continente_origem

            with c2:
                paises = get_unique("RotasVoo", 'pais_origem', filters=[f"continente_origem = '{continente_origem}'"])
                pais_origem = st.selectbox("País", paises, index=None, key='pais_origem')

    if pais_origem:
        with st.container(border=True):
            st.subheader("Destino")
            c3, c4 = st.columns(2)
            filters['pais_origem'] = pais_origem


            continentes = get_unique("RotasVoo", 'continente_destino', filters=[f"pais_origem = '{pais_origem}'"])

            with c3:
                continente_destino = st.selectbox("Continente", continentes, index=None, key='continente_destino')
                if continente_destino:
                    filters['continente_destino'] = continente_destino

        if continente_destino:
            with c4:
                paises = get_unique("RotasVoo", 'pais_destino', filters={'pais_origem':pais_origem, "continente_destino":continente_destino})
                pais_destino = st.selectbox("País", paises, index=None, key='pais_destino')
                if pais_destino:
                    filters['pais_destino'] = pais_destino

    return filters
            
        
