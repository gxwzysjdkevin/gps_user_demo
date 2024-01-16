# -*- coding: utf-8 -*-
"""
@author: ababa
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.preprocessing import MinMaxScaler

def normalize_data(dataset):
    scaler = MinMaxScaler()
    dataset['date'] = pd.to_datetime(dataset.iloc[:, 0]).dt.date
    grouped = dataset.groupby('date')
    for _, group in grouped:
        group_index = group.index
        dataset.iloc[group_index, 1:-1] = scaler.fit_transform(group.iloc[:, 1:-1])
    dataset.drop('date', axis=1, inplace=True)

# Set global font to Times New Roman for all plots
matplotlib.rcParams['font.family'] = 'Times New Roman'

# Reading car-hailing flow data
df_dc = pd.read_csv(r"...\10_workday_dc.csv")

# Reading total flow data
df_flow = pd.read_csv(r"...\10_workday_flow.csv")

# Normalize each day's data
# Initialize MinMaxScaler
scaler = MinMaxScaler()
datasets = [df_flow, df_dc]

# Normalize each dataset day-wise
for dataset in datasets:
    # Convert first column to datetime and extract date for grouping
    dataset.iloc[:, 0] = pd.to_datetime(dataset.iloc[:, 0])
    dataset['date_1'] = dataset.iloc[:, 0].dt.date
    grouped = dataset.groupby('date_1')

    # Normalize each group
    for name, group in grouped:
        group_index = group.index
        dataset.iloc[group_index, 1:-1] = scaler.fit_transform(group.iloc[:, 1:-1])

    # Remove auxiliary date column after normalization
    dataset.drop('date_1', axis=1, inplace=True)

# Convert first column to datetime for further processing
df_dc.iloc[:, 0] = pd.to_datetime(df_dc.iloc[:, 0])
df_flow.iloc[:, 0] = pd.to_datetime(df_flow.iloc[:, 0])

# Generate time series for every 15 minutes of each workday in October
october_dates = pd.date_range('2016-10-01', '2016-10-31')

# Generate time series for every 15 minutes during the National holiday
national_holiday = pd.date_range('2016-10-01', '2016-10-07 23:45', freq='15T')

# Define weekend dates
weekends_dates = ['2016-10-15', '2016-10-16', '2016-10-22', '2016-10-23', '2016-10-29', '2016-10-30']

# Create empty DatetimeIndex for weekends
weekends = pd.DatetimeIndex([])

# Populate weekends with 15-minute intervals
for date in weekends_dates:
    weekends = weekends.union(pd.date_range(date, date + ' 23:45', freq='15T'))

# Extract workday dates by excluding weekends and holidays from October dates
workdays_dates = october_dates.difference(national_holiday.union(weekends))

# Create empty DatetimeIndex for workdays
workdays = pd.DatetimeIndex([])

# Populate workdays with 15-minute intervals
for date in workdays_dates:
    workdays = workdays.union(pd.date_range(date, pd.Timestamp(date).strftime('%Y-%m-%d') + ' 23:45', freq='15T'))

# Filter the datasets for workdays
df_flow_workdays = df_flow[df_flow.iloc[:, 0].isin(workdays)]
df_dc_workdays = df_dc[df_dc.iloc[:, 0].isin(workdays)]

# Function to draw scatter plots for flow and congestion
def draw_figure(time, flow, congestion):
    # Convert time to 15-minute intervals and use as X-axis labels
    time_intervals = time.strftime('%H:%M')

    # Set scatter plot size
    scatter_size = 2

    # Create plot and axes
    fig, ax1 = plt.subplots()

    # Plot car-hailing flow on the first axis
    ax1.scatter(time_intervals, flow, s=scatter_size, color='b')
    ax1.set_ylabel('Car-hailing Flow (Normalization)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Create a second axis sharing the same X-axis
    ax2 = ax1.twinx()
    ax2.scatter(time_intervals, congestion, s=scatter_size, color='r')
    ax2.set_ylabel('Degree of Congestion (Normalization)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # Set X-axis ticks and labels for hourly intervals
    hourly_intervals = time_intervals[::8]  # Take every 8th point for hourly intervals
    ax1.set_xticks(hourly_intervals)
    ax1.set_xticklabels(hourly_intervals, rotation=45)

    # Display the plot
    plt.show()

# Call the function with workdays, and flow and congestion data
draw_figure(workdays, df_flow_workdays.iloc[:, 1], df_dc_workdays.iloc[:, 1])

