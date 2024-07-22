from handlers.utilities.streamlit_utils import convert_df_to_csv
import streamlit as st

def download_button(dataframe, file_name='results.csv', location=st):

    # Download button
    location.download_button(
        label=f"Download as CSV (Total: {len(dataframe)})",
        data=convert_df_to_csv(dataframe),
        file_name=file_name,
        mime="text/csv",
    )