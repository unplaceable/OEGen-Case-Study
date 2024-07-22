import streamlit as st
from pydantic import ValidationError

from handlers.utilities.slack import new_pipeline_alert
from SETTINGS import TECHNOLOGY_TYPES, RAG_STATUS, PIPELINE_STATUS
from data_models.models import Pipeline, Counterparty, InformationPoint


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

            capacity = st.number_input('Capacity (MWp)', min_value=0)

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
            'Capacity': capacity,
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


def create_counterparty_form():

    with st.expander("Create a new counterparty"):
        with st.form("add_counterparty_form"):
            counterparty_name = st.text_input('Counterparty name', max_chars=100)
            
            ceo_name = st.text_input('CEO', max_chars=100)

            strategy = st.text_input('Strategy', max_chars=100)


            platform_lead = st.text_input('Platform lead', max_chars=100)

            deal_lead = st.text_input('Deal lead', max_chars=100)

            finance_lead = st.text_input('Finance lead', max_chars=100)

            new_counterparty_submitted = st.form_submit_button("Submit")

    if new_counterparty_submitted:
        try:
            Counterparty({
                'CounterpartyName': counterparty_name,
                'CEO': ceo_name,
                'Strategy': strategy,
                'PlatformLead': platform_lead,
                'DealLead': deal_lead,
                'FinanceLead': finance_lead
            })
            st.toast(f'New counterparty created: {counterparty_name}', icon="✅")
        except ValidationError as exc:
            st.error(f"{repr(exc.errors()[0]['loc'])}: {repr(exc.errors()[0]['msg'])}")
            st.stop()
    


def create_information_point_form():

    with st.expander("Create a new Information Point"):
        with st.form("add_information_point_form"):

            title = st.text_input('Title', max_chars=100)
            
            description = st.text_area('Description', max_chars=500)

            market = st.text_input('Market', max_chars=100)

            technology = st.radio('Technology', options=TECHNOLOGY_TYPES, index=None)

            all_counterparties = [counterparty['CounterpartyName'] for counterparty in Counterparty().get_all(return_type='raw')]
            counterparties = str(st.multiselect('Counterparties', options=all_counterparties))

            impact = st.slider("Impact (1-100)", min_value=1, max_value=100, value=1)

            likelihood = st.slider("Likelihood (1-100)", min_value=1, max_value=100, value=1)

            new_information_point_submitted = st.form_submit_button("Submit")

    if new_information_point_submitted:
        try:
            InformationPoint({
                'Title': title,
                'Description': description,
                'Market': market,
                'Technology': technology,
                'Counterparties': counterparties,
                'Impact': impact,
                'Likelihood': likelihood
            })
        except ValidationError as exc:
            st.error(f"{repr(exc.errors()[0]['loc'])}: {repr(exc.errors()[0]['msg'])}")
            st.stop()


        st.toast(f'New information point created: {title}', icon="✅")