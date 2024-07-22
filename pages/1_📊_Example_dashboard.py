import streamlit as st

import time


from components.graphs import cumulative_pipeline_capacity, pipeline_heatmap, likelihood_vs_impact_scatter, top_ten_information_points_by_rating
from components.maps import pipeline_locations_with_capacity_and_rag
from data_models.models import Pipeline, InformationPoint

pipeline_data = Pipeline().get_all()

st.set_page_config(page_title="Example Dashboard", page_icon="📊")
st.title("📊 Example Dashboard")


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



# Capacity forecasting
st.markdown('### Cumulative Capacity Forecasting with 5-Year Predictions Based on Last 5 Years')
st.write('Below shows the historic cumulative capacity, with a prediction of the next 5 using using a rolling average of the previous 5 years.')
cumulative_pipeline_capacity(pipeline_data)

# Map
st.markdown('### Pipeline Locations')
# st.markdown('>### Key\n >- Height: Total capacity\n >- Colour: RAG Status')
st.write('Below shows the geo-distribution of pipeline locations. The colour represents the RAGSTatus, the height represents the capacity.')
pipeline_locations_with_capacity_and_rag(pipeline_data)

# Technlogy and status heatmap
st.markdown('### Capacity Heatmap by Technology and Status')
st.write('Heatmap showing the relationship between pipeline statuses and technology')
pipeline_heatmap(pipeline_data)




all_information_points = InformationPoint().get_all()
col1, col2 = st.columns(2)
with col1:
    st.markdown('### Likelihood vs Impact for Information Points')
    likelihood_vs_impact_scatter(all_information_points)

with col2:
    st.markdown('### Top 10 Information Points by Rating')
    top_ten_information_points_by_rating(all_information_points)


col1, col2 = st.columns(2)
with col1:
    # Technology distribution
    st.markdown('### Pipeline Sources')
    grouped_df = pipeline_data.groupby('Technology')[['Capacity']].sum()
    st.write('Total capacity in pipelines for each technology source')
    st.bar_chart(data=grouped_df, y_label='Capacity')

with col2:
    # Status distribution
    st.markdown('### Pipeline statuses')
    grouped_df = pipeline_data.groupby('ProjectStatus')['ID'].count()
    st.write('Total number of pipelines for each pipeline status')
    st.bar_chart(data=grouped_df, y_label='No. pipelines')


