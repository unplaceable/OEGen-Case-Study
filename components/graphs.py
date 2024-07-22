import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def cumulative_pipeline_capacity(pipeline_df):

    # Convert RTBDate to datetime
    pipeline_df['RTBDate'] = pd.to_datetime(pipeline_df['RTBDate'], errors='coerce')
    if pipeline_df['RTBDate'].isnull().any():
        raise ValueError('There are invalid date entries in the RTBDate column.')

    # Pivot the data to aggregate capacity by type and date
    pivot_df = pipeline_df.pivot_table(index='RTBDate', columns='Technology', values='Capacity', aggfunc='sum').fillna(0)
    pivot_df = pivot_df.reset_index()

    # Compute cumulative sums for each type
    pivot_df['CumulativeSolarCapacity'] = pivot_df['Solar'].cumsum()
    pivot_df['CumulativeWindCapacity'] = pivot_df['Wind'].cumsum()
    pivot_df['CumulativeBESSCapacity'] = pivot_df['BESS'].cumsum()

    # Compute Total Capacity
    pivot_df['TotalCapacity'] = (pivot_df['CumulativeSolarCapacity'] +
                                 pivot_df['CumulativeWindCapacity'] +
                                 pivot_df['CumulativeBESSCapacity'])

    # Prepare data for filtering (only past 5 years)
    latest_date = pivot_df['RTBDate'].max()
    five_years_ago = latest_date - pd.DateOffset(years=5)
    filtered_pivot_df = pivot_df[pivot_df['RTBDate'] >= five_years_ago]

    # Prepare data for linear regression on the past 5 years
    filtered_pivot_df['Days'] = (filtered_pivot_df['RTBDate'] - filtered_pivot_df['RTBDate'].min()).dt.days

    # Fit linear regression models on the last 5 years of data
    models = {
        'SolarCapacity': LinearRegression(),
        'WindCapacity': LinearRegression(),
        'BESSCapacity': LinearRegression(),
        'TotalCapacity': LinearRegression()
    }

    for metric in models:
        X = filtered_pivot_df[['Days']]
        y = filtered_pivot_df[f'Cumulative{metric}'] if metric != 'TotalCapacity' else filtered_pivot_df['TotalCapacity']
        models[metric].fit(X, y)

    # Predict future values (5 years ahead)
    days_ahead = 5 * 365  # 5 years in days
    future_days = np.arange(filtered_pivot_df['Days'].max() + 1, filtered_pivot_df['Days'].max() + days_ahead + 1)
    future_dates = pd.date_range(start=latest_date + pd.Timedelta(days=1), periods=days_ahead)

    # Generate predictions
    predictions = {metric: models[metric].predict(future_days.reshape(-1, 1)) for metric in models}

    # Plot the cumulative data with a secondary Y-axis and prediction lines
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot cumulative solar, wind, and BESS capacities from entire dataset
    ax1.plot(pivot_df['RTBDate'], pivot_df['CumulativeSolarCapacity'], label='Cumulative Solar Capacity', marker='o', color='b')
    ax1.plot(pivot_df['RTBDate'], pivot_df['CumulativeWindCapacity'], label='Cumulative Wind Capacity', marker='o', color='g')
    ax1.plot(pivot_df['RTBDate'], pivot_df['CumulativeBESSCapacity'], label='Cumulative BESS Capacity', marker='o', color='r')

    # Create a secondary Y-axis for Total Capacity
    ax2 = ax1.twinx()
    ax2.plot(pivot_df['RTBDate'], pivot_df['TotalCapacity'], label='Total Capacity', marker='x', color='purple', linestyle='--')

    # Plot the predictions for all metrics including Total Capacity
    ax1.plot(future_dates, predictions['SolarCapacity'], label='Predicted Cumulative Solar Capacity (5 Years)', linestyle='--', color='blue')
    ax1.plot(future_dates, predictions['WindCapacity'], label='Predicted Cumulative Wind Capacity (5 Years)', linestyle='--', color='green')
    ax1.plot(future_dates, predictions['BESSCapacity'], label='Predicted Cumulative BESS Capacity (5 Years)', linestyle='--', color='red')
    ax2.plot(future_dates, predictions['TotalCapacity'], label='Predicted Total Capacity (5 Years)', linestyle='--', color='orange')

    # Labeling and titles
    ax1.set_xlabel('RTB Date')
    ax1.set_ylabel('Cumulative Capacity')
    ax1.set_title('Cumulative Capacity Forecasting with 5-Year Predictions Based on Last 5 Years')
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # Secondary Y-axis for Total Capacity
    ax2.set_ylabel('Total Capacity', color='purple')
    ax2.legend(loc='upper right')

    # Streamlit app
    st.pyplot(fig)


def pipeline_heatmap(pipeline_df):

    # Create a pivot table for the heatmap
    pivot_table = pipeline_df.pivot_table(values='Capacity', index='Technology', columns='ProjectStatus', aggfunc='sum', fill_value=0)

    # Create a heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='Viridis'))

    fig.update_layout(
        title='Capacity Heatmap by Technology and Status',
        xaxis_nticks=36,
        yaxis_nticks=36,
        xaxis_title='Project Status',
        yaxis_title='Technology')

    # Display the heatmap
    st.plotly_chart(fig)



def likelihood_vs_impact_scatter(information_points):

    fig, ax = plt.subplots()
    ax.scatter(information_points['Impact'], information_points['Likelihood'], color='blue')
    ax.set_xlabel('Impact')
    ax.set_ylabel('Likelihood')
    ax.set_title('Impact vs Likelihood')

    # Display the plot
    st.pyplot(fig)


def top_ten_information_points_by_rating(information_points):

    top_10_df = information_points.nlargest(10, 'Rating').sort_values(by='Rating', ascending=True)

    # Plotting with matplotlib
    fig, ax = plt.subplots()
    ax.barh(top_10_df['Title'], top_10_df['Rating'], color='skyblue')
    ax.set_xlabel('Rating')
    ax.set_title('Top 10 Information Pipelines by Rating')

    # Display the plot in Streamlit
    st.pyplot(fig)