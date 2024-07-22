import streamlit as st

@st.cache_data
def convert_df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun

    return df.to_csv().encode("utf-8")