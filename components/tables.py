
import streamlit as st



def pipeline_table(pipelines):
    
    # Change the ProjectName column to be a link
    pipelines['ProjectName'] = pipelines.apply(
                                            lambda row: f'<a href="/Pipelines?pipeline_id={row["ID"]}">{row["ProjectName"]}</a>', 
                                            axis=1
                                        )

    # Filter DataFrame to only include the specified columns
    columns_to_include = [
        "ProjectName", "Technology", "Capacity", "ProjectStatus", "RAGStatus",
    ]
    df_filtered = pipelines[columns_to_include]

    st.write(df_filtered.to_html(escape=False, index=False), unsafe_allow_html=True)


def counterparty_table(counterparties):

    # Change the ProjectName column to be a link
    counterparties['CounterpartyName'] = counterparties.apply(
                                            lambda row: f'<a href="/Counterparties?counterparty_id={row["ID"]}">{row["CounterpartyName"]}</a>', 
                                            axis=1
                                        )

    # Filter DataFrame to only include the specified columns
    columns_to_include = [
        "CounterpartyName", "CEO", "LastModified"
    ]
    df_filtered = counterparties[columns_to_include]

    st.write(df_filtered.to_html(escape=False, index=False), unsafe_allow_html=True)


def information_point_table(information_points):



    # Change the ProjectName column to be a link
    information_points['Title'] = information_points.apply(
                                            lambda row: f'<a href="/Information_points?information_point_id={row["ID"]}">{row["Title"]}</a>', 
                                            axis=1
                                        )

    # Filter DataFrame to only include the specified columns
    columns_to_include = [
        "Title", "Market", "Impact", "Likelihood", "Rating"
    ]
    df_filtered = information_points[columns_to_include]

    st.write(df_filtered.to_html(escape=False, index=False), unsafe_allow_html=True)
