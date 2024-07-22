import streamlit as st

import time


from components.graphs import cumulative_pipeline_capacity
from components.maps import pipeline_locations_with_capacity_and_rag
from data_models.models import Pipeline

pipeline_data = Pipeline().get_all()

st.set_page_config(page_title="Pipeline Dashboard", page_icon="📊")
st.title("📊 Pipeline Dashboard")


# Chat
with st.sidebar:

    with st.expander("Ask AI", expanded=True):
    
        messages = st.container(height=300)
        messages.chat_message("assistant").write('Ask me about the data on this page')
        if prompt := st.chat_input("Say something...", max_chars=200):
            messages.chat_message("user").write(prompt)
            time.sleep(1)
            
            messages.chat_message("assistant").write(f"Quantum Quarries has the largest capacity at 62.052MWp. It uses Wind.")
        st.markdown('*The above is a simulation only, I lost access to the account that has OpenAI credits.*')

# Map
st.markdown('### Locations')
# st.markdown('>### Key\n >- Height: Total capacity\n >- Colour: RAG Status')
st.write('Below shows the geo-distribution of pipeline locations. The colour represents the RAGSTatus, the height represents the capacity.')

pipeline_locations_with_capacity_and_rag(pipeline_data)

# Capacity forecasting
st.markdown('### Cumulative Capacity Forecasting with 5-Year Predictions Based on Last 5 Years')
st.write('Below shows the historic cumulative capacity, with a prediction of the next 5 using using a rolling average of the previous 5 years.')
cumulative_pipeline_capacity(pipeline_data)


col1, col2 = st.columns(2)

with col1:
    # Technology distribution
    st.markdown('### Sources')
    grouped_df = pipeline_data.groupby('Technology')[['SolarCapacity', 'WindCapacity', 'BESSCapacity']].sum()

    st.bar_chart(data=grouped_df)

with col2:
    # Status distribution
    st.markdown('### Statuses')
    grouped_df = pipeline_data.groupby('ProjectStatus')['ID'].count()

    st.bar_chart(data=grouped_df)


