import streamlit as st
import pydeck as pdk
import time

from handlers.data.db import Data
from components.forms import create_pipeline_form
from data_models.models import Pipeline, Counterparty, Audit
from components.tables import pipeline_table
from components.buttons import download_button
from SETTINGS import TECHNOLOGY_TYPES, RAG_STATUS, PIPELINE_STATUS


if "pipeline_id" in st.query_params:

    pipeline = Pipeline().get_by_id(st.query_params['pipeline_id'])[0]
    counterparty = Counterparty().get_by_id(pipeline['CounterpartyID'])[0]
    
    pipeline['CounterpartyName']=counterparty['CounterpartyName']

    page_icon_lookup = {
        'Solar': '☀️',
        'Wind': '💨',
        'BESS': '🔋'
    }

    page_icon=page_icon_lookup[pipeline['Technology']] or '?'
    project_name=pipeline['ProjectName']

    st.set_page_config(page_title=project_name, page_icon=page_icon)
    st.title(f'{page_icon} {project_name}')

    if "view_type" not in st.query_params or st.query_params['view_type']=='view':
        st.link_button("Edit", f"/Pipelines?pipeline_id={pipeline['ID']}&view_type=edit")
    st.subheader(f"with {counterparty['CounterpartyName']}")

    # Latest comment
    if pipeline['RAGStatus']=='Red':
        st.error(pipeline['RAGComment'])
    else:
        st.info(pipeline['RAGComment'])

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Technology", value=pipeline['Technology'])
    col2.metric(label="Progress", value=pipeline['ProjectStatus'])
    col3.metric(label="Capacity", value=f'{pipeline["Capacity"]} MWp')

    st.header('Pipeline info')
    if "view_type" not in st.query_params or st.query_params['view_type']=='view':
        # Table data
        st.table(data=pipeline)
    else:
        edited_df = st.data_editor(
        [pipeline],
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
    
    st.header('Counterparty')
    st.link_button('View', f"/Counterparties?counterparty_id={counterparty['ID']}")
    st.table(data=counterparty)

    audit_history = Audit.get_history(counterparty['ID'])
    st.header('Audit history')
    st.table(data=audit_history)
        

else:
    st.set_page_config(page_title="Pipeline search", page_icon="🔎")
    st.title(f"🔎 Pipeline search")

    create_pipeline_form()

    search_text = st.text_input('', max_chars=100, placeholder='Search (eg, Solar)')

    if search_text:

        results = Pipeline().search(search_text, include_columns=['ID', 'ProjectName','Technology','ProjectStatus', 'RAGStatus', 'RTBDate'])

        if len(results)==0:
            st.write('Nothing found')
        else:
            download_button(results, file_name='pipelines.csv')
            pipeline_table(results)
    else:
        all_pipelines = Pipeline().get_all()
        download_button(all_pipelines, file_name='pipelines.csv')
        pipeline_table(all_pipelines)
