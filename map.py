import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

def color_marker(frequency, min_frequency, max_frequency):
    normalized_freq = (frequency - min_frequency) / (max_frequency - min_frequency)
    color = (int(normalized_freq * 200), int((1 - normalized_freq) * 128), 0)
    return '#%02x%02x%02x' % color

@st.cache_data
def load_map_data(file_path):
    return pd.read_csv(file_path)


def plot_locations(df):
    
    min_frequency = df['Frequency'].min()
    max_frequency = df['Frequency'].max()

    max_freq_location = df.loc[df['Frequency'].idxmax()]
    map_center = (max_freq_location['Latitude'], max_freq_location['Longitude'])

    my_map = folium.Map(location=map_center, zoom_start=6)
    
    for idx, row in df.iterrows():
        location = (row['Latitude'], row['Longitude'])
        marker_size = np.log(row['Frequency'] ) * 3
        folium.CircleMarker(
            location=location,
            radius=marker_size,
            color=color_marker(row['Frequency'], min_frequency, max_frequency),
            fill=True,
            fill_color=color_marker(row['Frequency'], min_frequency, max_frequency),
            fill_opacity=0.5,
            popup=f"<b>{row['Location']}</b><br>Frequency: {row['Frequency']}",
        ).add_to(my_map)

    folium_static(my_map)


st.set_page_config(layout="wide")
st.title("Location Visualization & Severity Maps")

# uploaded_map_file = st.file_uploader("Upload CSV file for Map Visualization", type=["csv"])

st.write("Turkey, 2023")
map_df1 = load_map_data('coordinate_turkey.csv')
plot_locations(map_df1)

st.write("Mexico, 2017")
map_df2 = load_map_data('coordinates_mexico.csv')
plot_locations(map_df2)

st.write("Iraq-Iran, 2017")
map_df3 = load_map_data('coordinate_iraq_iran.csv')
plot_locations(map_df3)