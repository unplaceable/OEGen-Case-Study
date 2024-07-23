import streamlit as st
import pydeck as pdk
import time

from data_models.models import Pipeline, Counterparty, InformationPoint
from components.tables import pipeline_table, counterparty_table, information_point_table


st.set_page_config(page_title="Search", page_icon="🔎")
st.title(f"🔎 Search")


# Create buttons
col1, col2, col3, col4 = st.columns([0.3, 0.4, 0.4, 0.1])
with col1:
    st.link_button('Create a new pipeline', '/Manage_pipelines')
with col2:
    st.link_button('Create a new counterparty', '/Manage_counterparties')  
with col3:
    st.link_button('Create a new information point', '/Manage_information_points')  

search_text = st.text_input('', max_chars=100, placeholder='Search (eg, Solar)')

if search_text:

    with st.spinner("Loading..."):
        time.sleep(1)

    
    # Pipeline results
    st.markdown('### Pipelines')
    results = Pipeline().search(search_text)

    if len(results)==0:
        st.write('Nothing found')
    else:
        pipeline_table(results)

    # Divider
    st.divider()

    # Counterparty results
    st.markdown('### Counterparties')
    results = Counterparty().search(search_text)

    if len(results)==0:
        st.write('Nothing found')
    else:
        counterparty_table(results)

    # Divider
    st.divider()

    # Information points results
    st.markdown('### Information points')
    results = InformationPoint().search(search_text)

    if len(results)==0:
        st.write('Nothing found')
    else:
        information_point_table(results)
