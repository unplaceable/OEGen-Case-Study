import streamlit as st
from pydantic import ValidationError

from handlers.utilities.slack import new_pipeline_alert
from SETTINGS import TECHNOLOGY_TYPES, RAG_STATUS, PIPELINE_STATUS
from data_models.models import Pipeline, Counterparty

def create_pipeline_form():

    with st.expander("Create a new pipeline"):
        with st.form("add_pipeline_form"):

            # Counterparties dropdown
            all_counterparties = Counterparty().get_all(return_type='raw')
            # all_counterparties.sort(key=operator.itemgetter('CounterpartyName')) # Sort the counterparties into alphabetical order
            counterparty_names = tuple([counterparty['CounterpartyName'] for counterparty in all_counterparties])
            options = list(range(len(counterparty_names)))
            value = st.selectbox("Counterparty", options=options, format_func=lambda x: counterparty_names[x])
            counterparty_id = [counterparty['ID'] for counterparty in all_counterparties][value]

            project_name = st.text_input('Project name', max_chars=100)
            
            longitude = st.text_input('Longitude', max_chars=100)
            latitude = st.text_input('Latitude', max_chars=100)

            technology = st.radio('Technology type', options=TECHNOLOGY_TYPES, index=None)

            solar_capacity = st.number_input('Solar capacity (MWp)', min_value=0)
            wind_capacity = st.number_input('Wind capacity (MWp)', min_value=0)
            bess_capacity = st.number_input('BESS capacity (MWp)', min_value=0)

            project_status = st.selectbox('Project status', options=PIPELINE_STATUS, index=None)

            rtb_date = st.date_input('RTB date', help='Ready to build date', format="YYYY-MM-DD")
            
            rag_status = st.selectbox('RAG status', options=RAG_STATUS, index=None)

            rag_comment = st.text_area('Comment', max_chars=1000)

            new_pipeline_submitted = st.form_submit_button("Submit")

    if new_pipeline_submitted:

        new_pipeline = {
            'CounterpartyID': counterparty_id,
            'ProjectName': project_name,
            'Long': longitude,
            'Lat': latitude,
            'Technology': technology,
            'SolarCapacity': solar_capacity,
            'WindCapacity': wind_capacity,
            'BESSCapacity': bess_capacity,
            'RTBDate': rtb_date,
            'RAGStatus': rag_status,
            'RAGComment': rag_comment,
            'ProjectStatus': project_status
            
        }

        try:
            new_pipeline = Pipeline(new_pipeline).data
            st.toast(f'New pipeline created: {project_name}', icon="✅")
        except ValidationError as exc:
            st.error(f"{repr(exc.errors()[0]['loc'])}: {repr(exc.errors()[0]['msg'])}")
            st.toast(f"{repr(exc.errors()[0]['loc'])}: {repr(exc.errors()[0]['msg'])}", icon="❌")
            st.stop()
        
        
        new_pipeline_alert(new_pipeline)