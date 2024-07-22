import streamlit as st
from pydantic import ValidationError

from data_models.models import InformationPoint, Counterparty
from handlers.utilities.streamlit_utils import convert_df_to_csv
from SETTINGS import TECHNOLOGY_TYPES

# information_points_data = InformationPoint().get_all()
counterparties_data = Counterparty().get_all(return_type='raw')


st.set_page_config(page_title="Information points", page_icon="ⓘ")
st.title("ⓘ Information points")






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


