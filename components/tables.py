
import streamlit as st



def pipeline_table(pipeline):
    
    # Function to render the text centered
    def centered_text(text):
        return f'<p style="text-align:center;">{text}</p>'

    # Add headers
    header_cols = st.columns([1, 2, 1, 1, 1])
    header_cols[0].markdown(centered_text("ProjectName"), unsafe_allow_html=True)
    header_cols[1].markdown(centered_text("Technology"), unsafe_allow_html=True)
    header_cols[2].markdown(centered_text("ProjectStatus"), unsafe_allow_html=True)
    header_cols[3].markdown(centered_text(""), unsafe_allow_html=True)
    header_cols[4].markdown(centered_text(""), unsafe_allow_html=True)

    # Add data rows
    for index, row in pipeline.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
        col1.markdown(centered_text(row["ProjectName"]), unsafe_allow_html=True)
        col2.markdown(centered_text(row["Technology"]), unsafe_allow_html=True)
        col3.markdown(centered_text(row["ProjectStatus"]), unsafe_allow_html=True)
        col4.link_button("View", f"/Pipeline?pipeline_id={row['ID']}")
        col5.link_button("Edit", f"/Pipeline?pipeline_id={row['ID']}&view_type=edit")


def counterparty_table(counterparty):
    
    # Function to render the text centered
    def centered_text(text):
        return f'<p style="text-align:center;">{text}</p>'

    # Add headers
    header_cols = st.columns([1, 2, 1, 1, 1])
    header_cols[0].markdown(centered_text("Name"), unsafe_allow_html=True)
    header_cols[1].markdown(centered_text("CEO"), unsafe_allow_html=True)
    header_cols[2].markdown(centered_text("LastModified"), unsafe_allow_html=True)
    header_cols[3].markdown(centered_text(""), unsafe_allow_html=True)
    header_cols[4].markdown(centered_text(""), unsafe_allow_html=True)

    # Add data rows
    for index, row in counterparty.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
        col1.markdown(centered_text(row["CounterpartyName"]), unsafe_allow_html=True)
        col2.markdown(centered_text(row["CEO"]), unsafe_allow_html=True)
        col3.markdown(centered_text(row["LastModified"]), unsafe_allow_html=True)
        col4.link_button("View", f"/Counterparty?counterparty_id={row['ID']}")
        col5.link_button("Edit", f"/Counterparty?counterparty_id={row['ID']}&view_type=edit")


def information_point_table(information_points):
    
    # Function to render the text centered
    def centered_text(text):
        return f'<p style="text-align:center;">{text}</p>'

    # Add headers
    header_cols = st.columns([1, 2, 1, 1, 1])
    header_cols[0].markdown(centered_text("Title"), unsafe_allow_html=True)
    header_cols[1].markdown(centered_text("Market"), unsafe_allow_html=True)
    header_cols[2].markdown(centered_text("Rating"), unsafe_allow_html=True)
    header_cols[3].markdown(centered_text(""), unsafe_allow_html=True)
    header_cols[4].markdown(centered_text(""), unsafe_allow_html=True)

    # Add data rows
    for index, row in information_points.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
        col1.markdown(centered_text(row["Title"]), unsafe_allow_html=True)
        col2.markdown(centered_text(row["Market"]), unsafe_allow_html=True)
        col3.markdown(centered_text(row["Rating"]), unsafe_allow_html=True)
        col4.link_button("View", f"/Information_point?information_point_id={row['ID']}")
        col5.link_button("Edit", f"/Information_point?information_point_id={row['ID']}&view_type=edit")
        
