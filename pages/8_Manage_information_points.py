import streamlit as st
from pydantic import ValidationError

from data_models.models import InformationPoint, Counterparty
from handlers.utilities.streamlit_utils import convert_df_to_csv
from SETTINGS import TECHNOLOGY_TYPES

# information_points_data = InformationPoint().get_all()
counterparties_data = Counterparty().get_all(return_type='raw')


st.set_page_config(page_title="Information points", page_icon="ⓘ")
st.title("ⓘ Information points")

with st.expander("Create a new Information Point"):
    with st.form("add_information_point_form"):

        title = st.text_input('Title', max_chars=100)
        
        description = st.text_area('Description', max_chars=500)

        market = st.text_input('Market', max_chars=100)

        technology = st.radio('Technology', options=TECHNOLOGY_TYPES, index=None)

        all_counterparties = [counterparty['CounterpartyName'] for counterparty in counterparties_data]
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

# Columns for text search and download
left, right = st.columns(2, vertical_alignment="bottom")

# Text search
search_text = left.text_input('', max_chars=100, placeholder='Search...')

if search_text:
    information_point_data = InformationPoint().search(search_text)
else:
    information_point_data=InformationPoint().get_all()

# Download button
right.download_button(
    label=f"Download as CSV (Total: {len(information_point_data)})",
    data=convert_df_to_csv(information_point_data),
    file_name="large_df.csv",
    mime="text/csv",
)

edited_df = st.data_editor(
    information_point_data,
    use_container_width=True,
    hide_index=True,
    disabled=["ID"]
)

# Counterparty().bulk_update(edited_df)


