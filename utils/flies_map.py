import streamlit as st
import pydeck as pdk
import airportsdata as ad

from utils.database import get_all

airports = ad.load()

def get_airport_cord(icao):
    try:
        airport = airports[icao]
        return [airport['lon'], airport['lat']]
    except:
        return None
    
{'mes':1}

def render_map():
    flies = get_all("VoosToMap")
    flies['cord_origem'] = flies['sigla_origem'].apply(get_airport_cord)
    flies['cord_destino'] = flies['sigla_destino'].apply(get_airport_cord)

    print(flies[['cord_origem', 'cord_destino']].head())

    layer = pdk.Layer(
        "GreatCircleLayer",
        flies,
        pickable=True,
        get_stroke_width=12,
        get_source_position="cord_origem",
        get_target_position="cord_destino",
        get_source_color=[64, 255, 0],
        get_target_color=[0, 128, 200],
        auto_highlight=True,
    )

    view_state = pdk.ViewState(latitude=50, longitude=-40, zoom=1, bearing=0, pitch=0)

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{nome_origem} to {nome_destino}"},
    )

    r.picking_radius = 10

    st.write(flies)

    st.pydeck_chart(r)
