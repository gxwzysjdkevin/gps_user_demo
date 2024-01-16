import pandas as pd
import osmnx as ox
import numpy as np
import math
import time

# Constants
EARTH_RADIUS = 6378.137  # Earth's radius in kilometers

# Function to convert degrees to radians
def to_radians(degrees):
    return degrees * math.pi / 180.0

# Function to calculate distance between two lat-lon points
def calculate_distance(lat1, lng1, lat2, lng2):
    radLat1 = to_radians(lat1)
    radLat2 = to_radians(lat2)
    delta_lat = radLat1 - radLat2
    delta_lng = to_radians(lng1) - to_radians(lng2)
    a = np.sin(delta_lat / 2) ** 2 + np.cos(radLat1) * np.cos(radLat2) * np.sin(delta_lng / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = c * EARTH_RADIUS * 1000  # Convert to meters
    return distance



# Date range
dates = range(20161001, 20161032)
dfnum = pd.DataFrame()
i = 0

for date in dates:
    print(date)
    try:
        start = time.time()
        file_name = f'gps_{date}.txt' # can be modified
        # Import file with column names
        file_path = fr'.../{file_name}'
        chunks = pd.read_csv(file_path, iterator=True, header=None, error_bad_lines=False)
        df = pd.concat(list(chunks), ignore_index=True)
        df.columns = ['vid', 'did', 'time', 'lon', 'lat']
        df.reset_index(drop=True, inplace=True)

        # OSMnx graph
        G = ox.graph_from_bbox(df.lat.max() + 0.01, df.lat.min() - 0.01, df.lon.max() + 0.01, df.lon.min() - 0.01, network_type='drive')
        nearest_edges = ox.get_nearest_edges(G, df.lon - 0.002427, df.lat + 0.002427, method='kdtree', dist=0.0005) # can be modified
        df_nearest = pd.DataFrame(nearest_edges, columns=['roadx', 'roady', 'key'])
        df = pd.concat([df, df_nearest], axis=1)

        # Traffic data aggregation
        min_time = df.time.min()
        for j in range(96):
            time_frame_start = j * 900 + min_time
            time_frame_end = time_frame_start + 900
            df_time_frame = df.query(f"time >= {time_frame_start} and time < {time_frame_end}")

            road_group = df_time_frame.groupby(['roadx', 'roady', 'did']).count().reset_index()[
                ['roadx', 'roady', 'did']]
            road_count = road_group.groupby(['roadx', 'roady']).count().reset_index()
            hour, mins = divmod(j * 15 + 15, 60)
            timestamp = f"{date} {hour:02d}:{mins:02d}:00"
            road_count.columns = ['roadx', 'roady', timestamp]
            road_count.set_index(road_count.roadx.astype('str') + ',' + road_count.roady.astype('str'), inplace=True)
            road_count.drop(columns=['roadx', 'roady'], inplace=True)

            dfnum = pd.merge(dfnum, road_count, left_index=True, right_index=True, how='outer')

        # Speed calculation
        for j in range(96):
            time_frame_start = j * 900 + min_time
            time_frame_end = time_frame_start + 900
            df_time_frame = df.query(f"time >= {time_frame_start} and time < {time_frame_end}")
            df_time_frame.sort_values(by=['roadx', 'roady', 'did', 'time'], inplace=True)
            df_time_frame.reset_index(drop=True, inplace=True)

            # Preparing data for speed calculation
            df_prev = df_time_frame.shift(1).fillna(0)
            df_time_frame['time_diff'] = df_time_frame['time'] - df_prev['time']
            df_time_frame['distance'] = df_time_frame.apply(
                lambda row: calculate_distance(row['lat'], row['lon'], df_prev.at[row.name, 'lat'],
                                               df_prev.at[row.name, 'lon']) if row['time_diff'] < 10 else 0,
                axis=1
            )
            df_speed = df_time_frame[df_time_frame['time_diff'] > 0]
            df_speed['average_speed'] = df_speed['distance'] / df_speed['time_diff']
            speed_group = df_speed.groupby(['roadx', 'roady']).mean()['average_speed']

            hour, mins = divmod(j * 15 + 15, 60)
            timestamp = f"{date} {hour:02d}:{mins:02d}:00"
            speed_group.name = timestamp
            dfspeed = pd.merge(dfspeed, speed_group, left_index=True, right_index=True,
                               how='outer') if j > 0 else speed_group.to_frame()

        end = time.time()
        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(end - start))
        print(f"Time taken for {date}: {elapsed_time}")
        i += 1

    except Exception as e:
        print(f"Error processing date {date}: {e}")
        i += 1
        continue

# Saving the final data
dfnum.to_csv(r'.../flow.csv')
dfspeed.to_csv(r'.../speed.csv')

