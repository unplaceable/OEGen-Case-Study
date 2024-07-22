import streamlit as st
from pydantic import ValidationError

from data_models.models import Counterparty
from handlers.utilities.streamlit_utils import convert_df_to_csv

counterparties_data = Counterparty().get_all()

st.set_page_config(page_title="Counterparties", page_icon="🏢")
st.title("🏢 Counterparties")




    

# Columns for text search and download
left, right = st.columns(2, vertical_alignment="bottom")

# Text search
search_text = left.text_input('', max_chars=100, placeholder='Search...')

if search_text:
    counterparty_data = Counterparty().search(search_text)
else:
    counterparty_data=Counterparty().get_all()

# Download button
right.download_button(
    label=f"Download as CSV (Total: {len(counterparty_data)})",
    data=convert_df_to_csv(counterparty_data),
    file_name="large_df.csv",
    mime="text/csv",
)

edited_df = st.data_editor(
    counterparty_data,
    use_container_width=True,
    hide_index=True,
    disabled=["ID"]
)

# Counterparty().bulk_update(edited_df)


