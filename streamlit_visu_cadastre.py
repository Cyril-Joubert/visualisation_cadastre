import streamlit as st
import pandas as pd
import pydeck as pdk

column_names = ['lieu', 'lon', 'lat', "cadastre"]
sism = pd.read_csv("sismique_grenoble_metropole.csv", sep=",", names=column_names)

inond = pd.read_csv("inondations_grenoble_metropole.csv", sep=",", names=column_names)

st.write("""
# Data visualisation
""")


layer_sism = pdk.Layer(
    'ScatterplotLayer',
    sism,
    get_position='[lon, lat]',
    get_radius=50,
    get_fill_color=[255, 0, 0],
    pickable=True,
    tooltip=True,
)

layer_inond = pdk.Layer(
    'ScatterplotLayer',
    inond,
    get_position='[lon, lat]',
    get_radius=50,
    get_fill_color=[0, 0, 255],
    pickable=True,
    tooltip=True,
)

deck_sism = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=sism['lat'].mean(),
        longitude=sism['lon'].mean(),
        zoom=9.5,
    ),
    layers=[layer_sism],
    tooltip={"html": "<b>Cadastre:</b> {cadastre}", "style": {"color": "white"}}
)

deck_inond = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=inond['lat'].mean(),
        longitude=inond['lon'].mean(),
        zoom=9.5,
    ),
    layers=[layer_inond],
    tooltip={"html": "<b>Cadastre:</b> {cadastre}", "style": {"color": "white"}}
)

st.write("## Seismic issues map:")
st.pydeck_chart(deck_sism)

sism_count = sism['lieu'].value_counts()
lieu_sism = sism_count.to_frame().sort_values(by="count", ascending=False)
st.write("### Number of issues by location:")
st.bar_chart(lieu_sism, color=[215, 30, 30])

sism_type = sism['cadastre'].value_counts()
cadastre_sism = sism_type.to_frame().sort_values(by="count", ascending=False)
st.write("### Number of issues by type:")
st.bar_chart(cadastre_sism, color=[215, 30, 30])

st.write("## Flood issues map:")
st.pydeck_chart(deck_inond)

inond_count = inond['lieu'].value_counts()
lieu_inond = inond_count.to_frame().sort_values(by="count", ascending=False)
st.write("### Number of issues by location:")
st.bar_chart(lieu_inond, color=[0, 0, 215])

inond_type = inond['cadastre'].value_counts()
cadastre_inond = inond_type.to_frame().sort_values(by="count", ascending=False)
st.write("### Number of issues by type:")
st.bar_chart(cadastre_inond, color=[0, 0, 215])
