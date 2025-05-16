
# import pandas as pd
# import plotly.express as px
# from dash import Dash, dcc, html, Input, Output
# import dash_bootstrap_components as dbc

# # Load and prepare data
# # df = pd.read_excel(r"C:\Users\hgada\OneDrive - Hearst\Documents\Log Summary Python\wdsu\WDSU.xlsx")
# df = pd.read_excel("WDSU.xlsx")

# df.columns = df.columns.str.strip()
# df = df.dropna(subset=['Aired Time', 'Sched Time', 'Program'])
# df['Aired Time'] = df['Aired Time'].astype(str).str.replace('XM', 'AM', case=False, regex=False)
# df['Sched Time'] = df['Sched Time'].astype(str).str.replace('XM', 'AM', case=False, regex=False)

# df['AiredTimeOnly'] = pd.to_datetime(df['Aired Time'], errors='coerce').dt.time
# df['SchedTimeOnly'] = pd.to_datetime(df['Sched Time'], errors='coerce').dt.time
# df = df.dropna(subset=['AiredTimeOnly', 'SchedTimeOnly'])

# def time_to_seconds(t):
#     return t.hour * 3600 + t.minute * 60 + t.second

# df['AiredSeconds'] = df['AiredTimeOnly'].apply(time_to_seconds)
# df['SchedSeconds'] = df['SchedTimeOnly'].apply(time_to_seconds)

# df['TimeInSeconds'] = abs(df['AiredSeconds'] - df['SchedSeconds'])
# df['TimeInSeconds'] = df['TimeInSeconds'].apply(lambda x: min(x, 86400 - x))

# df['TimeDifferenceFormatted'] = df['TimeInSeconds'].apply(lambda x: f"{int(x // 60):02d}:{int(x % 60):02d}")

# # Dynamically get max minutes from data (rounded up)
# max_minutes = int(df['TimeInSeconds'].max() // 60) + 1  # e.g., 84 if max is 83.3 mins

# app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# app.title = "Time Difference Explorer"

# app.layout = dbc.Container([
#     html.H2("Select Minimum Time Difference Threshold (minutes)", className="my-3 text-center"),

#     dcc.RangeSlider(
#         id='time-diff-slider',
#         min=0,
#         max=max_minutes,
#         step=1,
#         value=[0, max_minutes],
#         marks={i: f'{i}' for i in range(0, max_minutes + 1, 10)},
#         tooltip={"placement": "bottom", "always_visible": True},
#         allowCross=False,
#         className="mb-4"
#     ),

#     dcc.Graph(id='bar-chart'),

#     html.Div(id='program-list', className="mt-4")
# ], fluid=True)


# @app.callback(
#     Output('bar-chart', 'figure'),
#     Input('time-diff-slider', 'value')
# )
# def update_chart(selected_range):
#     min_sec = selected_range[0] * 60
#     max_sec = selected_range[1] * 60
#     filtered_df = df[(df['TimeInSeconds'] >= min_sec) & (df['TimeInSeconds'] <= max_sec)]

#     agg_df = filtered_df.groupby('TimeDifferenceFormatted').agg(
#         Count=('TimeDifferenceFormatted', 'size')
#     ).reset_index()

#     agg_df = agg_df.sort_values(by='Count', ascending=False)

#     title_text = f"Counts of Time Differences between {selected_range[0]} and {selected_range[1]} minutes"
#     fig = px.bar(
#         agg_df,
#         x='TimeDifferenceFormatted',
#         y='Count',
#         title=title_text,
#         labels={'TimeDifferenceFormatted': 'Time Difference (MM:SS)', 'Count': 'Count'},
#         template='plotly_dark'
#     )
#     fig.update_xaxes(tickangle=-45)
#     return fig


# @app.callback(
#     Output('program-list', 'children'),
#     Input('bar-chart', 'clickData'),
#     Input('time-diff-slider', 'value')
# )
# def display_programs(clickData, selected_range):
#     if clickData:
#         clicked_time = clickData['points'][0]['x']
#         min_sec = selected_range[0] * 60
#         max_sec = selected_range[1] * 60
#         filtered_df_range = df[(df['TimeInSeconds'] >= min_sec) & (df['TimeInSeconds'] <= max_sec)]

#         filtered_programs = filtered_df_range[filtered_df_range['TimeDifferenceFormatted'] == clicked_time][['Program', 'Aired Time', 'Sched Time']]
#         if filtered_programs.empty:
#             return html.Div(f"No programs found for time difference {clicked_time} in selected range.")
        
#         return html.Div([
#             html.H4(f"Programs with Time Difference {clicked_time}"),
#             html.Ul([
#                 html.Li(f"{row['Program']} | Aired: {row['Aired Time']} | Scheduled: {row['Sched Time']}")
#                 for _, row in filtered_programs.iterrows()
#             ])
#         ])
#     return html.Div("Click a bar to see programs.")


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')

#final:

# import pandas as pd
# import plotly.express as px
# from dash import Dash, dcc, html, Input, Output
# import dash_bootstrap_components as dbc

# # Load and prepare data
# df = pd.read_excel("WDSU.xlsx")

# df.columns = df.columns.str.strip()
# df = df.dropna(subset=['Aired Time', 'Sched Time', 'Program'])
# df['Aired Time'] = df['Aired Time'].astype(str).str.replace('XM', 'AM', case=False, regex=False)
# df['Sched Time'] = df['Sched Time'].astype(str).str.replace('XM', 'AM', case=False, regex=False)

# df['AiredTimeOnly'] = pd.to_datetime(df['Aired Time'], errors='coerce').dt.time
# df['SchedTimeOnly'] = pd.to_datetime(df['Sched Time'], errors='coerce').dt.time
# df = df.dropna(subset=['AiredTimeOnly', 'SchedTimeOnly'])

# def time_to_seconds(t):
#     return t.hour * 3600 + t.minute * 60 + t.second

# df['AiredSeconds'] = df['AiredTimeOnly'].apply(time_to_seconds)
# df['SchedSeconds'] = df['SchedTimeOnly'].apply(time_to_seconds)

# df['TimeInSeconds'] = abs(df['AiredSeconds'] - df['SchedSeconds'])
# df['TimeInSeconds'] = df['TimeInSeconds'].apply(lambda x: min(x, 86400 - x))

# df['TimeDifferenceFormatted'] = df['TimeInSeconds'].apply(lambda x: f"{int(x // 60):02d}:{int(x % 60):02d}")

# max_minutes = int(df['TimeInSeconds'].max() // 60) + 1

# app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# server = app.server  # <-- This line is necessary for hosting platforms like Heroku
# app.title = "Time Difference Explorer"

# app.layout = dbc.Container([
#     html.H2("Select Minimum Time Difference Threshold (minutes)", className="my-3 text-center"),

#     dcc.RangeSlider(
#         id='time-diff-slider',
#         min=0,
#         max=max_minutes,
#         step=1,
#         value=[0, max_minutes],
#         marks={i: f'{i}' for i in range(0, max_minutes + 1, 10)},
#         tooltip={"placement": "bottom", "always_visible": True},
#         allowCross=False,
#         className="mb-4"
#     ),

#     dcc.Graph(id='bar-chart'),

#     html.Div(id='program-list', className="mt-4")
# ], fluid=True)


# @app.callback(
#     Output('bar-chart', 'figure'),
#     Input('time-diff-slider', 'value')
# )
# def update_chart(selected_range):
#     min_sec = selected_range[0] * 60
#     max_sec = selected_range[1] * 60
#     filtered_df = df[(df['TimeInSeconds'] >= min_sec) & (df['TimeInSeconds'] <= max_sec)]

#     agg_df = filtered_df.groupby('TimeDifferenceFormatted').agg(
#         Count=('TimeDifferenceFormatted', 'size')
#     ).reset_index()

#     agg_df = agg_df.sort_values(by='Count', ascending=False)

#     title_text = f"Counts of Time Differences between {selected_range[0]} and {selected_range[1]} minutes"
#     fig = px.bar(
#         agg_df,
#         x='TimeDifferenceFormatted',
#         y='Count',
#         title=title_text,
#         labels={'TimeDifferenceFormatted': 'Time Difference (MM:SS)', 'Count': 'Count'},
#         template='plotly_dark'
#     )
#     fig.update_xaxes(tickangle=-45)
#     return fig


# @app.callback(
#     Output('program-list', 'children'),
#     Input('bar-chart', 'clickData'),
#     Input('time-diff-slider', 'value')
# )
# def display_programs(clickData, selected_range):
#     if clickData:
#         clicked_time = clickData['points'][0]['x']
#         min_sec = selected_range[0] * 60
#         max_sec = selected_range[1] * 60
#         filtered_df = df[(df['TimeInSeconds'] >= min_sec) & (df['TimeInSeconds'] <= max_sec)]

#         programs = filtered_df[filtered_df['TimeDifferenceFormatted'] == clicked_time]['Program'].unique()
#         if len(programs) == 0:
#             return html.Div(f"No programs found for time difference {clicked_time} in selected range.")
#         return html.Div([
#             html.H4(f"Programs with Time Difference {clicked_time}"),
#             html.Ul([html.Li(p) for p in programs])
#         ])
#     return html.Div("Click a bar to see programs.")


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')


# #http://127.0.0.1:8050/


#for streamlit
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load and clean the data
df = pd.read_excel("WDSU.xlsx")

df.columns = df.columns.str.strip()
df = df.dropna(subset=['Aired Time', 'Sched Time', 'Program'])
df['Aired Time'] = df['Aired Time'].astype(str).str.replace('XM', 'AM', case=False, regex=False)
df['Sched Time'] = df['Sched Time'].astype(str).str.replace('XM', 'AM', case=False, regex=False)

df['AiredTimeOnly'] = pd.to_datetime(df['Aired Time'], errors='coerce').dt.time
df['SchedTimeOnly'] = pd.to_datetime(df['Sched Time'], errors='coerce').dt.time
df = df.dropna(subset=['AiredTimeOnly', 'SchedTimeOnly'])

def time_to_seconds(t):
    return t.hour * 3600 + t.minute * 60 + t.second

df['AiredSeconds'] = df['AiredTimeOnly'].apply(time_to_seconds)
df['SchedSeconds'] = df['SchedTimeOnly'].apply(time_to_seconds)

df['TimeInSeconds'] = abs(df['AiredSeconds'] - df['SchedSeconds'])
df['TimeInSeconds'] = df['TimeInSeconds'].apply(lambda x: min(x, 86400 - x))

df['TimeDifferenceFormatted'] = df['TimeInSeconds'].apply(lambda x: f"{int(x // 60):02d}:{int(x % 60):02d}")

# Streamlit UI
st.set_page_config(page_title="Time Difference Explorer", layout="wide")
st.title("Time Difference Explorer")

# Slider for selecting range
min_val, max_val = st.slider(
    "Select Time Difference Range (minutes)",
    0, int(df['TimeInSeconds'].max() // 60) + 1,
    (0, int(df['TimeInSeconds'].max() // 60) + 1),
    step=1
)

min_sec = min_val * 60
max_sec = max_val * 60
filtered_df = df[(df['TimeInSeconds'] >= min_sec) & (df['TimeInSeconds'] <= max_sec)]

agg_df = filtered_df.groupby('TimeDifferenceFormatted').size().reset_index(name='Count')
agg_df = agg_df.sort_values(by='Count', ascending=False)

# Plot
fig = px.bar(
    agg_df,
    x='TimeDifferenceFormatted',
    y='Count',
    title=f"Time Differences between {min_val} and {max_val} minutes",
    labels={'TimeDifferenceFormatted': 'Time Difference (MM:SS)', 'Count': 'Count'}
)
fig.update_xaxes(tickangle=-45)

clicked = st.plotly_chart(fig, use_container_width=True)

# Select time to see programs (simulate "click")
selected_time = st.selectbox("Select a Time Difference to view matching programs:", agg_df['TimeDifferenceFormatted'])

if selected_time:
    matched_programs = filtered_df[filtered_df['TimeDifferenceFormatted'] == selected_time]['Program'].unique()
    st.subheader(f"Programs with Time Difference {selected_time}")
    if len(matched_programs) == 0:
        st.info("No matching programs found.")
    else:
        st.write(matched_programs)

