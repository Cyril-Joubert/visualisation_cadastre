import streamlit as st
import pandas as pd
import pydeck as pdk

def update_map_view(selected_commune):
    selected_data = sele[sele['commune'] == selected_commune]
    new_view_state = pdk.ViewState(
        latitude=selected_data['y_latitude'].mean(),
        longitude=selected_data['x_longitude'].mean(),
        zoom=12
    )
    return new_view_state


if __name__ == "__main__":

    column_names = ['lieu', 'lon', 'lat', "probleme"]
    sism = pd.read_csv("sismique_grenoble_metropole.csv", sep=",", names=column_names)

    inond = pd.read_csv("inondations_grenoble_metropole.csv", sep=",", names=column_names)

    sele = pd.read_csv("sele_metro.csv", sep=",")

    st.write("""
    # Data visualization
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

    layer_sele = pdk.Layer(
        'ScatterplotLayer',
        sele,
        get_position='[x_longitude, y_latitude]',
        get_radius=50,
        get_fill_color=[0, 255, 0],
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
        tooltip={"html": "<b>Problème:</b> {probleme}", "style": {"color": "white"}}
    )

    deck_inond = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=inond['lat'].mean(),
            longitude=inond['lon'].mean(),
            zoom=9.5,
        ),
        layers=[layer_inond],
        tooltip={"html": "<b>Problème:</b> {probleme}", "style": {"color": "white"}}
    )

    deck_sele = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=sele['y_latitude'].mean(),
            longitude=sele['x_longitude'].mean(),
            zoom=9.5,
        ),
        layers=[layer_sele],
        tooltip={"html": "<b>Type de dechet collecté:</b> {type_dechet}<br><b>Commune: </b> {commune}", "style": {"color": "white"}}
    )

    st.write("## Seismic issues map:")
    st.pydeck_chart(deck_sism)

    sism_count = sism['lieu'].value_counts()
    lieu_sism = sism_count.to_frame().sort_values(by="count", ascending=False)
    st.write("### Number of issues by location:")
    st.bar_chart(lieu_sism, color=[215, 30, 30])

    sism_type = sism['probleme'].value_counts()
    cadastre_sism = sism_type.to_frame().sort_values(by="count", ascending=False)
    st.write("### Number of issues by type:")
    st.bar_chart(cadastre_sism, color=[215, 30, 30])

    st.write("## Flood issues map:")
    st.pydeck_chart(deck_inond)

    inond_count = inond['lieu'].value_counts()
    lieu_inond = inond_count.to_frame().sort_values(by="count", ascending=False)
    st.write("### Number of issues by location:")
    st.bar_chart(lieu_inond, color=[0, 0, 215])

    inond_type = inond['probleme'].value_counts()
    cadastre_inond = inond_type.to_frame().sort_values(by="count", ascending=False)
    st.write("### Number of issues by type:")
    st.bar_chart(cadastre_inond, color=[0, 0, 215])

    st.write("## Waste container map:")
    selected_commune = st.selectbox('Choisir une commune : ', sele["commune"].sort_values().unique(), index=sele["commune"].sort_values().unique().tolist().index("Grenoble"))
    view_state = update_map_view(selected_commune)
    updated_deck_sele = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer_sele],
        tooltip={"html": "<b>Type de dechet collecté:</b> {type_dechet}<br><b>Commune: </b> {commune}", "style": {"color": "white"}}
    )
    st.pydeck_chart(updated_deck_sele)

    container_count = sele['commune'].value_counts()
    cont = container_count.to_frame().sort_values(by="count", ascending=False)
    st.write("### Number of waste container by town:")
    st.bar_chart(cont, color=[0, 215, 0])

    type_count = sele['type_dechet'].value_counts()
    type = type_count.to_frame().sort_values(by="count", ascending=False)
    st.write("### Type of waste container:")
    st.bar_chart(type, color=[0, 215, 0])
