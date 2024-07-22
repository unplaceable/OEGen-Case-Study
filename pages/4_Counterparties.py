import streamlit as st
import pydeck as pdk
import time

from handlers.data.db import Data
from data_models.models import Pipeline, Counterparty, Audit
from components.tables import pipeline_table, counterparty_table
from components.buttons import download_button
from components.forms import create_counterparty_form
from SETTINGS import TECHNOLOGY_TYPES, RAG_STATUS, PIPELINE_STATUS




if "counterparty_id" in st.query_params:

    counterparty = Counterparty().get_by_id(st.query_params['counterparty_id'])[0]

    st.set_page_config(page_title=counterparty['CounterpartyName'], page_icon="🏢")
    st.title(f'{counterparty["CounterpartyName"]}')

    col1, col2 = st.columns(2)
    col1.metric(label="CEO", value=counterparty['CEO'])
    col2.metric(label="Created", value=counterparty['Created'])

    st.header('Counterparty info')
    if "view_type" not in st.query_params or st.query_params['view_type']=='view':
        # Table data
        st.table(data=counterparty)
    else:
        edited_df = st.data_editor(
        [counterparty],
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
    
    st.header('Pipelines')
    # st.table(data=)


    pipeline_table(Pipeline().search(counterparty['ID']))

    audit_history = Audit.get_history(counterparty['ID'])
    st.header('Audit history')
    st.table(data=audit_history)


else:
    st.set_page_config(page_title="Counterparty search", page_icon="🔎")
    st.title(f"🔎 Counterparty search")

    create_counterparty_form()
    search_text = st.text_input('', max_chars=100, placeholder='Search (eg, Blue Ocean)')

    if search_text:
        results = Counterparty().search(search_text, include_columns=['ID', 'CounterpartyName', 'CEO', 'LastModified'])

        if len(results)==0:
            st.write('Nothing found')
        else:
            download_button(results, file_name='counterparties.csv')
            counterparty_table(results)
    else:
        all_counterparties=Counterparty().get_all()
        download_button(all_counterparties, file_name='counterparties.csv')
        counterparty_table(all_counterparties)