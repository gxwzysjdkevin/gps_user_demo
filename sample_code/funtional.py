# -*- coding: utf-8 -*-
"""
@author: ababa
"""
import numpy as np
import pandas as pd
import os

def process_speed_data(data, threshold):
    """
    Processes the given DataFrame to handle values over threshold.
    For values over threshold, it checks the adjacent columns (left and right) and
    if both are below threshold, replaces the value with their average.
    Otherwise, it replaces with the lower of the two values if below threshold.

    Parameters:
    data (pd.DataFrame): DataFrame containing speed data.
    threshold (float): input parameters, speed limit

    Returns:
    pd.DataFrame: Processed DataFrame with adjusted values.
    """
    for column_index, column in enumerate(data.columns):
        mask = data[column] > threshold
        if mask.any():
            # Find row indices with values over threshold
            row_indices = np.where(mask)[0]

            # Get values from adjacent columns
            left_value = data.iloc[row_indices, column_index - 1] if column_index > 0 else data.iloc[row_indices, column_index]
            right_value = data.iloc[row_indices, column_index + 1] if column_index < data.shape[1] - 1 else data.iloc[row_indices, column_index]

            # Check if both adjacent values are below threshold
            both_below_threshold = (left_value < threshold) & (right_value < threshold)

            # Calculate mean of adjacent values
            mean_values = (left_value + right_value) / 2

            # Replace values over threshold with mean or the lower of the two adjacent values
            data.loc[mask, column] = np.where(both_below_threshold, mean_values, np.where(left_value < threshold, left_value, right_value))

    return data

# Example usage
# speed_data_interpolated = pd.DataFrame(...)  # data
# processed_data = process_speed_data(speed_data_interpolated)

def calculate_inrix_congestion(speed_file_path, length_file_path):
    """
    Calculate INRIX congestion scores based on speed and length data.

    Parameters:
    speed_file_path (str): File path for the speed data CSV.
    length_file_path (str): File path for the road length data CSV.

    Returns:
    pd.DataFrame: DataFrame with road data, congestion scores, and weighted average result.
    """
    # Read data from CSV files
    df_speed = pd.read_csv(speed_file_path)
    df_length = pd.read_csv(length_file_path)

    # Extract road data
    road_columns = ['roadx', 'roady']
    road_data = df_speed[road_columns]

    # Extract speed data
    speed_data = df_speed.iloc[:, 2:]

    # Calculate free flow speed as 85th percentile of speed values
    free_flow_speed = speed_data.quantile(0.85, axis=1)

    # Calculate congestion scores
    congestion_scores = free_flow_speed.div(speed_data.T).T - 1
    congestion_scores.clip(lower=0, inplace=True)

    # Merge road data with congestion scores
    merged_data = pd.concat([road_data, congestion_scores], axis=1)

    # Calculate weighted average congestion
    A_column_vector = df_length.iloc[:, 2].values.reshape(-1, 1)
    weighted_average_congestion = np.sum(A_column_vector * congestion_scores, axis=0) / np.sum(df_length.iloc[:, 2])

    return merged_data, weighted_average_congestion

# Example usage:
# speed_path = 'path_to_speed_data.csv'
# length_path = 'path_to_length_data.csv'
# merged_data_inrix, weighted_avg_inrix = calculate_inrix_congestion(speed_path, length_path)


