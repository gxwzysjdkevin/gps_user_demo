# GPS User Demo for Traffic Estimation

## Overview
This repository contains scripts and datasets aimed at estimating urban traffic patterns using GPS trace data from car-hailing services. Our framework leverages Python and pandas to process and analyze GPS data, providing insights into urban traffic flows and car-hailing fleet dynamics.

## Contents
- `generate_speed_flow.py`: Estimates traffic speed and flow based on GPS data.
- `functional.py`: Handles speed values that exceed the speed limit threshold and calculates the degree of congestion.
- `flow_speed_analysis.py`: Analyzes the differential patterns between car-hailing fleet and urban traffic flow. This script visualizes and compares the dynamics of traffic flow and speed, emphasizing the distinct behaviors and characteristics of car-hailing services versus general urban traffic.

## Getting Started

### Prerequisites
Ensure you have Python 3.x installed on your system along with pandas, numpy, matplotlib for data visualization, and other necessary libraries. You can install them using pip:


### Running the Examples
To run the example scripts and see how the framework processes and analyzes GPS data, follow these steps:

1. **Prepare your data**: Ensure your GPS data is formatted correctly. The expected format should include columns for anonymized driver ID, order ID, timestamp (Unix timestamp in seconds), and the corresponding latitude and longitude (GCJ coordinates).

2. **Estimate Traffic Speed and Flow**:
    ```
    python generate_speed_flow.py
    ```
   This script reads the formatted GPS data and applies algorithms to estimate traffic speed and flow. 

3. **Analyze Congestion**:
    ```
    python functional.py
    ```
   This script takes the output from `generate_speed_flow.py` and calculates congestion levels based on speed thresholds.

4. **Visualize Traffic Patterns**:
    ```
    python flow_speed_analysis.py
    ```
   Use this script to visualize and compare the traffic patterns of car-hailing services and general urban traffic. It helps highlight differences in carhailing fleet and urban traffic dynamic, providing insights into how car-hailing impacts urban traffic management.

### Example Data
 Due to confidentiality, we provide processed sample data instead of raw GPS data, available in the `data/` directory. This dataset includes urban network congestion levels and traffic flows for October 2016, enabling analysis of car-hailing versus general traffic patterns, a key contribution of our study.


