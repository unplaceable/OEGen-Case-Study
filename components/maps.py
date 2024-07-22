import streamlit as st
import pydeck as pdk


def pipeline_locations_with_capacity_and_rag(pipeline_df):

    # Define a function to get fill color based on RAGStatus
    def get_fill_color(status):
        if status == "Red":
            return [255, 0, 0]
        elif status == "Amber":
            return [255, 165, 0]
        else:
            return [0, 255, 0]

    # Apply the function to the dataframe
    pipeline_df["fill_color"] = pipeline_df["RAGStatus"].apply(get_fill_color)

    # Define the Pydeck Layer
    layer = pdk.Layer(
        "ColumnLayer",
        data=pipeline_df,
        get_position=["Long", "Lat"],
        get_elevation="Capacity",
        elevation_scale=1000,
        radius=10000,
        get_fill_color="fill_color",
        pickable=True,
        auto_highlight=True,
    )

    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=-2.0,
        latitude=54.0,
        zoom=5,
        pitch=50,
    )

    # Render the deck.gl map
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{ProjectName}\nCapacity: {Capacity} MW\nStatus: {RAGStatus}\nLat: {Lat}\nLong: {Long}"}
    )

    # Display the map in Streamlit
    st.pydeck_chart(deck)