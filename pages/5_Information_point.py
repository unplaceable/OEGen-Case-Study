import streamlit as st
import pydeck as pdk
import time

from data_models.models import InformationPoint
from components.tables import information_point_table
from SETTINGS import TECHNOLOGY_TYPES, RAG_STATUS, PIPELINE_STATUS


if "information_point_id" in st.query_params:

    information_point = InformationPoint().get_by_id(st.query_params['information_point_id'])[0]

    st.set_page_config(page_title=information_point['Title'], page_icon='ⓘ')
    st.title(f'ⓘ {information_point["Title"]}')

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Market", value=information_point['Technology'])
    col2.metric(label="Rating", value=information_point['Rating'])
    col3.metric(label="Market", value=information_point['Market'])

    if "view_type" not in st.query_params or st.query_params['view_type']=='view':
        # Table data
        st.table(data=information_point)
    else:
        edited_df = st.data_editor(
        [information_point],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Technology": st.column_config.SelectboxColumn(
                "Technology",
                options=TECHNOLOGY_TYPES,
                required=True,
            ),
            "RAGStatus": st.column_config.SelectboxColumn(
                "RAG Status",
                options=RAG_STATUS,
                required=True,
            ),
            "ProjectStatus": st.column_config.SelectboxColumn(
                "Project Status",
                options=PIPELINE_STATUS,
                required=True,
            )
        },
        # Disable editing the ID and Date Submitted columns.
        disabled=["ID"]
    )
        





else:
    st.set_page_config(page_title="Information points search", page_icon="🔎")
    st.title(f"🔎 Information points search")

    st.link_button('Create a new information point', '/Manage_information_points')
    search_text = st.text_input('', max_chars=100, placeholder='Search (eg, Solar)')

    if search_text:
        results = InformationPoint().search(search_text)

        if len(results)==0:
            st.write('Nothing found')

        information_point_table(results)
