import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

datasets = ["Haiti","Turkey-Syria","Mexico","Iraq-Iran","Japan"]
def plot_3d_data(x, y, z, t, datasets):
    fig = go.Figure()
    for i in range(len(x)):
        fig.add_trace(go.Scatter3d(
            x=[x[i]],
            y=[y[i]],
            z=[t[i]],
            mode='markers',
            marker=dict(
                size=np.log(np.pi * (z[i] * 500) ** 6),
                color=z[i],
                colorscale='Plasma',
                opacity=0.5,
                
            ),
            text=f"Location: {datasets[i]}, Date: {x[i]}, Magnitude: {y[i]}, Tweets: {t[i]}",
            hoverinfo='text',
            name=datasets[i]
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Time'),
            yaxis=dict(title='Magnitude'),
            zaxis=dict(title='Tweets')
        ),
        title='3D Dataset Visualization',
        coloraxis=dict(
            colorbar=dict(
                x=0,
                y=0.5,
                len=0.5,
                title='Z Value',
            )
        )
    )
    return fig

df_haiti = pd.read_csv('data/0f_haiti.csv', parse_dates=['date'], dayfirst=True)

df_turkey = pd.read_csv('data/0f_turkey.csv', parse_dates=['date'])

df_mexico = pd.read_csv('data/0f_mexico.csv')
df_mexico['date'] = pd.to_datetime(df_mexico['date'], format='%d_%m_%Y')

df_iraq = pd.read_csv('data/0f_iraq_iran.csv')
df_iraq['date'] = pd.to_datetime(df_iraq['date'], format='%d_%m_%Y')

df_japan = pd.read_csv('data/0f_japan.csv')
df_japan['date'] = pd.to_datetime(df_japan['date'], format='%b-%d')
df_japan['date'] = df_japan['date'].apply(lambda x: x.replace(year=2024))


earthquake_data = {
    'Date': ['2010-01-12', '2023-02-06', '2017-09-19', '2017-11-12','2024-01-01'],
    'Magnitude': [7.0, 7.8, 7.1, 7.3, 7.6]
}

earthquake_data['Date'] = pd.to_datetime(earthquake_data['Date'])
total_rows = len(df_haiti) + len(df_turkey) + len(df_mexico) + len(df_iraq) + len(df_japan)
num_rows = [len(df_haiti) / total_rows, len(df_turkey) / total_rows, len(df_mexico) / total_rows, len(df_iraq) / total_rows,len(df_japan) / total_rows]
t = [len(df_haiti), len(df_turkey), len(df_mexico), len(df_iraq), len(df_japan)]

st.title('Different Datasets')

fig = plot_3d_data(earthquake_data['Date'], earthquake_data['Magnitude'], num_rows, t, datasets)
st.plotly_chart(fig)

dfs = [df_haiti, df_turkey, df_mexico, df_iraq, df_japan]
datasets = ["Haiti", "Turkey-Syria", "Mexico", "Iraq-Iran", "Japan"]
colors = px.colors.qualitative.Plotly

st.title('Number of Entries per day')
fig_entries_per_date = px.line()
for i, df in enumerate(dfs):
    df_entries_per_date = df.groupby(df['date'].dt.date).size().reset_index(name='text')
    fig_entries_per_date.add_scatter(x=df_entries_per_date['date'], y=df_entries_per_date['text'], mode='markers+lines', name=datasets[i])
fig_entries_per_date.update_layout(xaxis_title='Date', yaxis_title='Number of Tweets', xaxis_tickangle=-45, legend_title="Datasets", showlegend=True, xaxis_rangeslider_visible=True)
st.plotly_chart(fig_entries_per_date)

st.title('Number of Entries per day (log-scaled)')
fig_entries_per_date_log = px.line()
for i, df in enumerate(dfs):
    df_entries_per_date = df.groupby(df['date'].dt.date).size().reset_index(name='text')
    df_entries_per_date['text'] = np.log(df_entries_per_date['text'] + 1)  
    fig_entries_per_date_log.add_scatter(x=df_entries_per_date['date'], y=df_entries_per_date['text'], mode='markers+lines', name=f'DF {i+1}')
fig_entries_per_date_log.update_layout(xaxis_title='Date', yaxis_title='Log(Number of Entries)', xaxis_tickangle=-45, legend_title="Datasets", showlegend=True, xaxis_rangeslider_visible=True)
st.plotly_chart(fig_entries_per_date_log)

for i, df in enumerate(dfs):
    df_entries_per_date = df.groupby(df['date'].dt.date).size().reset_index(name='text')
    fig_entries_per_date = px.line(df_entries_per_date, x='date', y='text', title=f'Number of Entries per day - {datasets[i]}', color_discrete_sequence=[colors[i]])
    fig_entries_per_date.update_layout(xaxis_title='Date', yaxis_title='Number of Tweets', xaxis_tickangle=0)
    st.plotly_chart(fig_entries_per_date)