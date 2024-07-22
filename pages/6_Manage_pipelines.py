import streamlit as st
from datetime import datetime
from pydantic import ValidationError

from components.forms import create_pipeline_form
from handlers.utilities.streamlit_utils import convert_df_to_csv
from SETTINGS import TECHNOLOGY_TYPES, RAG_STATUS, PIPELINE_STATUS
from data_models.models import Pipeline, Counterparty

pipeline_data = Pipeline().get_all()

st.set_page_config(page_title="Pipelines", page_icon="🚀")
st.title("🚀 Pipelines")


create_pipeline_form()

# Columns for text search and download
left, right = st.columns(2, vertical_alignment="bottom")

# Text search
search_text = left.text_input('', max_chars=100, placeholder='Search...')

if search_text:
    pipeline_data = Pipeline().search(search_text)
else:
    pipeline_data=Pipeline().get_all()

# Download button
right.download_button(
    label=f"Download as CSV (Total: {len(pipeline_data)})",
    data=convert_df_to_csv(pipeline_data),
    file_name="large_df.csv",
    mime="text/csv",
)

# Editable table
edited_df = st.data_editor(
    pipeline_data,
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

Pipeline().bulk_update(edited_df)