import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LinearRegression
import numpy as np




def cumulative_pipeline_capacity(pipeline_df):

    # Convert RTBDate to datetime
    pipeline_df['RTBDate'] = pd.to_datetime(pipeline_df['RTBDate'], errors='coerce')
    if pipeline_df['RTBDate'].isnull().any():
        raise ValueError('There are invalid date entries in the RTBDate column.')

    # Aggregate capacity data by RTBDate
    capacity_df = pipeline_df.groupby('RTBDate').agg({
        'SolarCapacity': 'sum',
        'WindCapacity': 'sum',
        'BESSCapacity': 'sum'
    }).reset_index()

    # Compute cumulative sums
    capacity_df['CumulativeSolarCapacity'] = capacity_df['SolarCapacity'].cumsum()
    capacity_df['CumulativeWindCapacity'] = capacity_df['WindCapacity'].cumsum()
    capacity_df['CumulativeBESSCapacity'] = capacity_df['BESSCapacity'].cumsum()

    # Compute Total Capacity
    capacity_df['TotalCapacity'] = (capacity_df['CumulativeSolarCapacity'] +
                                    capacity_df['CumulativeWindCapacity'] +
                                    capacity_df['CumulativeBESSCapacity'])

    # Prepare data for filtering (only past 5 years)
    latest_date = capacity_df['RTBDate'].max()
    five_years_ago = latest_date - pd.DateOffset(years=5)
    filtered_capacity_df = capacity_df[capacity_df['RTBDate'] >= five_years_ago]

    # Prepare data for linear regression on the past 5 years
    filtered_capacity_df['Days'] = (filtered_capacity_df['RTBDate'] - filtered_capacity_df['RTBDate'].min()).dt.days

    # Fit linear regression models on the last 5 years of data
    models = {
        'SolarCapacity': LinearRegression(),
        'WindCapacity': LinearRegression(),
        'BESSCapacity': LinearRegression(),
        'TotalCapacity': LinearRegression()
    }

    for metric in models:
        X = filtered_capacity_df[['Days']]
        y = filtered_capacity_df[f'Cumulative{metric}'] if metric != 'TotalCapacity' else filtered_capacity_df['TotalCapacity']
        models[metric].fit(X, y)

    # Predict future values (5 years ahead)
    days_ahead = 5 * 365  # 5 years in days
    future_days = np.arange(filtered_capacity_df['Days'].max() + 1, filtered_capacity_df['Days'].max() + days_ahead + 1)
    future_dates = pd.date_range(start=latest_date + pd.Timedelta(days=1), periods=days_ahead)

    # Generate predictions
    predictions = {metric: models[metric].predict(future_days.reshape(-1, 1)) for metric in models}

    # Plot the cumulative data with a secondary Y-axis and prediction lines
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot cumulative solar, wind, and BESS capacities from entire dataset
    ax1.plot(capacity_df['RTBDate'], capacity_df['CumulativeSolarCapacity'], label='Cumulative Solar Capacity', marker='o', color='b')
    ax1.plot(capacity_df['RTBDate'], capacity_df['CumulativeWindCapacity'], label='Cumulative Wind Capacity', marker='o', color='g')
    ax1.plot(capacity_df['RTBDate'], capacity_df['CumulativeBESSCapacity'], label='Cumulative BESS Capacity', marker='o', color='r')

    # Create a secondary Y-axis for Total Capacity
    ax2 = ax1.twinx()
    ax2.plot(capacity_df['RTBDate'], capacity_df['TotalCapacity'], label='Total Capacity', marker='x', color='purple', linestyle='--')

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