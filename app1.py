
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
st.title("📺 Time Difference Explorer")

# Time range slider
min_val, max_val = st.slider(
    "Select Time Difference Range (minutes)",
    0, int(df['TimeInSeconds'].max() // 60) + 1,
    (0, int(df['TimeInSeconds'].max() // 60) + 1),
    step=1
)
min_sec = min_val * 60
max_sec = max_val * 60

# Program filter
all_programs = sorted(df['Program'].unique())
with st.expander("🎛️ Program Filter"):
    select_all_programs = st.checkbox("Select All Programs", value=True)

    if select_all_programs:
        selected_programs = st.multiselect(
            "Choose programs to include (one below the other):",
            options=all_programs,
            default=all_programs,
            label_visibility="visible",
            max_selections=len(all_programs)  # ensures full list can be selected
        )
    else:
        selected_programs = st.multiselect(
            "Choose programs to include (one below the other):",
            options=all_programs,
            label_visibility="visible"
        )

# Sorting options
col1, col2 = st.columns(2)
with col1:
    sort_column = st.radio("Sort by:", options=["Time Difference", "Count"], index=1)
with col2:
    sort_order = st.radio("Sort Order:", options=["Descending", "Ascending"])
ascending = sort_order == "Ascending"

# Apply filters
filtered_df = df[
    (df['TimeInSeconds'] >= min_sec) &
    (df['TimeInSeconds'] <= max_sec) &
    (df['Program'].isin(selected_programs))
]

# Aggregate for chart
agg_df = filtered_df.groupby('TimeDifferenceFormatted').size().reset_index(name='Count')

if sort_column == "Count":
    agg_df = agg_df.sort_values(by='Count', ascending=ascending)
else:
    agg_df['Seconds'] = agg_df['TimeDifferenceFormatted'].apply(
        lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])
    )
    agg_df = agg_df.sort_values(by='Seconds', ascending=ascending)

# Plot
fig = px.bar(
    agg_df,
    x='TimeDifferenceFormatted',
    y='Count',
    title=f"Time Differences between {min_val} and {max_val} minutes",
    labels={'TimeDifferenceFormatted': 'Time Difference (MM:SS)', 'Count': 'Count'}
)
fig.update_xaxes(tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# Show matching programs
if not agg_df.empty:
    selected_time = st.selectbox("Select a Time Difference to view matching programs:", agg_df['TimeDifferenceFormatted'])
    matched_programs = filtered_df[filtered_df['TimeDifferenceFormatted'] == selected_time]['Program'].unique()
    
    st.subheader(f"Programs with Time Difference {selected_time}")
    if len(matched_programs) == 0:
        st.info("No matching programs found.")
    else:
        st.write(pd.DataFrame(matched_programs, columns=["Program"]))
else:
    st.warning("No data matches the selected filters.")
