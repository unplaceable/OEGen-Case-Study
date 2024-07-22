import streamlit as st
from pydantic import ValidationError

from data_models.models import Counterparty
from handlers.utilities.streamlit_utils import convert_df_to_csv

counterparties_data = Counterparty().get_all()

st.set_page_config(page_title="Counterparties", page_icon="🏢")
st.title("🏢 Counterparties")

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
    except ValidationError as exc:
        st.error(f"{repr(exc.errors()[0]['loc'])}: {repr(exc.errors()[0]['msg'])}")
        st.stop()


    st.toast(f'New counterparty created: {counterparty_name}', icon="✅")

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


