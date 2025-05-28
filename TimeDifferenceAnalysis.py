# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # from datetime import datetime

# # st.set_page_config(page_title="Time Difference Explorer", layout="wide")
# # st.title("📺 Time Difference Explorer")

# # # --- Dataset Selection ---
# # dataset_option = st.selectbox("Choose Dataset", ["WDSU", "WBAL", "WBAL - Part2"])

# # if dataset_option == "WDSU":
# #     file_path = "WDSU.xlsx"
# # elif dataset_option == "WBAL":
# #     file_path = "WBAL.xlsx"
# # else:
# #     file_path = r"C:\Users\hgada\OneDrive - Hearst\Documents\Log Summary Python\materials\wdsufinal\WBAL- Part2.xlsx"

# # # --- Load and Clean Data ---
# # df = pd.read_excel(file_path)
# # df.columns = df.columns.str.strip()
# # df = df.dropna(subset=['Aired Time', 'Sched Time', 'Program'])

# # # Clean time strings
# # df['Aired Time'] = df['Aired Time'].astype(str).str.replace('XM', 'AM', case=False, regex=False)
# # df['Sched Time'] = df['Sched Time'].astype(str).str.replace('XM', 'AM', case=False, regex=False)

# # # Parse times
# # df['AiredTimeOnly'] = pd.to_datetime(df['Aired Time'], errors='coerce').dt.time
# # df['SchedTimeOnly'] = pd.to_datetime(df['Sched Time'], errors='coerce').dt.time
# # df = df.dropna(subset=['AiredTimeOnly', 'SchedTimeOnly'])

# # # Convert time to seconds
# # def time_to_seconds(t):
# #     return t.hour * 3600 + t.minute * 60 + t.second

# # df['AiredSeconds'] = df['AiredTimeOnly'].apply(time_to_seconds)
# # df['SchedSeconds'] = df['SchedTimeOnly'].apply(time_to_seconds)

# # # Calculate absolute difference
# # df['TimeInSeconds'] = abs(df['AiredSeconds'] - df['SchedSeconds'])
# # df['TimeInSeconds'] = df['TimeInSeconds'].apply(lambda x: min(x, 86400 - x))

# # # Format as MM:SS
# # df['TimeDifferenceFormatted'] = df['TimeInSeconds'].apply(lambda x: f"{int(x // 60):02d}:{int(x % 60):02d}")

# # # --- Optional Air Date ---
# # if 'Air Date' in df.columns:
# #     df['AirDateOnly'] = pd.to_datetime(df['Air Date'], errors='coerce').dt.date
# #     df = df.dropna(subset=['AirDateOnly'])  # Drop rows with blank or invalid Air Date
# # else:
# #     df['AirDateOnly'] = None

# # # --- Time Range Slider ---
# # min_val, max_val = st.slider(
# #     "Select Time Difference Range (minutes)",
# #     0, int(df['TimeInSeconds'].max() // 60) + 1,
# #     (0, int(df['TimeInSeconds'].max() // 60) + 1),
# #     step=1
# # )
# # min_sec = min_val * 60
# # max_sec = max_val * 60

# # # --- Program Filter ---
# # all_programs = sorted(df['Program'].unique())
# # with st.expander("🎛️ Program Filter"):
# #     select_all_programs = st.checkbox("Select All Programs", value=True)

# #     if select_all_programs:
# #         selected_programs = st.multiselect(
# #             "Choose programs to include (one below the other):",
# #             options=all_programs,
# #             default=all_programs,
# #             label_visibility="visible"
# #         )
# #     else:
# #         selected_programs = st.multiselect(
# #             "Choose programs to include (one below the other):",
# #             options=all_programs,
# #             label_visibility="visible"
# #         )

# # # --- Day Filter (if available) ---
# # if 'AirDateOnly' in df.columns:
# #     all_dates = sorted(df['AirDateOnly'].unique())
# #     with st.expander("📅 Air Date Filter"):
# #         selected_dates = st.multiselect(
# #             "Select Air Dates to include:",
# #             options=all_dates,
# #             default=all_dates
# #         )
# # else:
# #     selected_dates = None

# # # --- Sorting Options ---
# # col1, col2 = st.columns(2)
# # with col1:
# #     sort_column = st.radio("Sort by:", options=["Time Difference", "Count"], index=1)
# # with col2:
# #     sort_order = st.radio("Sort Order:", options=["Descending", "Ascending"])
# # ascending = sort_order == "Ascending"

# # # --- Apply Filters ---
# # filtered_df = df[
# #     (df['TimeInSeconds'] >= min_sec) &
# #     (df['TimeInSeconds'] <= max_sec) &
# #     (df['Program'].isin(selected_programs))
# # ]
# # if selected_dates is not None:
# #     filtered_df = filtered_df[filtered_df['AirDateOnly'].isin(selected_dates)]

# # # --- Aggregate for Chart ---
# # agg_df = filtered_df.groupby('TimeDifferenceFormatted').size().reset_index(name='Count')

# # if sort_column == "Count":
# #     agg_df = agg_df.sort_values(by='Count', ascending=ascending)
# # else:
# #     agg_df['Seconds'] = agg_df['TimeDifferenceFormatted'].apply(
# #         lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])
# #     )
# #     agg_df = agg_df.sort_values(by='Seconds', ascending=ascending)

# # # --- Plot ---
# # fig = px.bar(
# #     agg_df,
# #     x='TimeDifferenceFormatted',
# #     y='Count',
# #     title=f"{dataset_option} - Time Differences between {min_val} and {max_val} minutes",
# #     labels={'TimeDifferenceFormatted': 'Time Difference (MM:SS)', 'Count': 'Count'}
# # )
# # fig.update_xaxes(tickangle=-45)
# # st.plotly_chart(fig, use_container_width=True)

# # # --- Show Matching Programs ---
# # if not agg_df.empty:
# #     selected_time = st.selectbox("Select a Time Difference to view matching programs:", agg_df['TimeDifferenceFormatted'])
# #     matched_programs = filtered_df[filtered_df['TimeDifferenceFormatted'] == selected_time]['Program'].unique()

# #     st.subheader(f"Programs with Time Difference {selected_time}")
# #     if len(matched_programs) == 0:
# #         st.info("No matching programs found.")
# #     else:
# #         st.write(pd.DataFrame(matched_programs, columns=["Program"]))
# # else:
# #     st.warning("No data matches the selected filters.")


# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from datetime import datetime

# st.set_page_config(page_title="Time Difference Explorer", layout="wide")
# st.title("📺 Time Difference Explorer")

# # --- Dataset Selection ---
# dataset_option = st.selectbox("Choose Dataset", ["WDSU", "WBAL", "WBAL - Part2"])

# if dataset_option == "WDSU":
#     file_path = "WDSU.xlsx"
# elif dataset_option == "WBAL":
#     file_path = "WBAL.xlsx"
# else:
#     file_path = r"C:\Users\hgada\OneDrive - Hearst\Documents\Log Summary Python\materials\wdsufinal\WBAL- Part2.xlsx"

# # --- Load and Clean Data ---
# df = pd.read_excel(file_path)
# df.columns = df.columns.str.strip()
# df = df.dropna(subset=['Aired Time', 'Sched Time', 'Program'])

# # Clean time strings
# df['Aired Time'] = df['Aired Time'].astype(str).str.replace('XM', 'AM', case=False, regex=False)
# df['Sched Time'] = df['Sched Time'].astype(str).str.replace('XM', 'AM', case=False, regex=False)

# # Parse times
# df['AiredTimeOnly'] = pd.to_datetime(df['Aired Time'], errors='coerce').dt.time
# df['SchedTimeOnly'] = pd.to_datetime(df['Sched Time'], errors='coerce').dt.time
# df = df.dropna(subset=['AiredTimeOnly', 'SchedTimeOnly'])

# # Convert time to seconds
# def time_to_seconds(t):
#     return t.hour * 3600 + t.minute * 60 + t.second

# df['AiredSeconds'] = df['AiredTimeOnly'].apply(time_to_seconds)
# df['SchedSeconds'] = df['SchedTimeOnly'].apply(time_to_seconds)

# # Calculate absolute difference
# df['TimeInSeconds'] = abs(df['AiredSeconds'] - df['SchedSeconds'])
# df['TimeInSeconds'] = df['TimeInSeconds'].apply(lambda x: min(x, 86400 - x))

# # Format as MM:SS
# df['TimeDifferenceFormatted'] = df['TimeInSeconds'].apply(lambda x: f"{int(x // 60):02d}:{int(x % 60):02d}")

# # --- Optional Air Date and Day Name ---
# if 'Air Date' in df.columns:
#     df['AirDateOnly'] = pd.to_datetime(df['Air Date'], errors='coerce').dt.date
#     df = df.dropna(subset=['AirDateOnly'])  # Drop rows with blank or invalid Air Date
#     df['DayName'] = pd.to_datetime(df['AirDateOnly']).dt.day_name()
# else:
#     df['AirDateOnly'] = None
#     df['DayName'] = None

# # --- Time Range Slider ---
# min_val, max_val = st.slider(
#     "Select Time Difference Range (minutes)",
#     0, int(df['TimeInSeconds'].max() // 60) + 1,
#     (0, int(df['TimeInSeconds'].max() // 60) + 1),
#     step=1
# )
# min_sec = min_val * 60
# max_sec = max_val * 60

# # --- Program Filter ---
# all_programs = sorted(df['Program'].unique())
# with st.expander("🎛️ Program Filter"):
#     select_all_programs = st.checkbox("Select All Programs", value=True)

#     if select_all_programs:
#         selected_programs = st.multiselect(
#             "Choose programs to include (one below the other):",
#             options=all_programs,
#             default=all_programs,
#             label_visibility="visible"
#         )
#     else:
#         selected_programs = st.multiselect(
#             "Choose programs to include (one below the other):",
#             options=all_programs,
#             label_visibility="visible"
#         )

# # --- Air Date and Day Name Filters (if available) ---
# if df['AirDateOnly'].notnull().any():
#     all_dates = sorted(df['AirDateOnly'].unique())
#     all_days = sorted(df['DayName'].dropna().unique())

#     with st.expander("📅 Air Date Filter"):
#         selected_dates = st.multiselect(
#             "Select Air Dates to include:",
#             options=all_dates,
#             default=all_dates
#         )

#     with st.expander("📆 Day Name Filter"):
#         selected_days = st.multiselect(
#             "Select Days to include:",
#             options=all_days,
#             default=all_days
#         )
# else:
#     selected_dates = None
#     selected_days = None

# # --- Sorting Options ---
# col1, col2 = st.columns(2)
# with col1:
#     sort_column = st.radio("Sort by:", options=["Time Difference", "Count"], index=1)
# with col2:
#     sort_order = st.radio("Sort Order:", options=["Descending", "Ascending"])
# ascending = sort_order == "Ascending"

# # --- Apply Filters ---
# filtered_df = df[
#     (df['TimeInSeconds'] >= min_sec) &
#     (df['TimeInSeconds'] <= max_sec) &
#     (df['Program'].isin(selected_programs))
# ]

# if selected_dates is not None:
#     filtered_df = filtered_df[filtered_df['AirDateOnly'].isin(selected_dates)]

# if selected_days is not None:
#     filtered_df = filtered_df[filtered_df['DayName'].isin(selected_days)]

# # --- Aggregate for Chart ---
# agg_df = filtered_df.groupby('TimeDifferenceFormatted').size().reset_index(name='Count')

# if sort_column == "Count":
#     agg_df = agg_df.sort_values(by='Count', ascending=ascending)
# else:
#     agg_df['Seconds'] = agg_df['TimeDifferenceFormatted'].apply(
#         lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])
#     )
#     agg_df = agg_df.sort_values(by='Seconds', ascending=ascending)

# # --- Plot ---
# fig = px.bar(
#     agg_df,
#     x='TimeDifferenceFormatted',
#     y='Count',
#     title=f"{dataset_option} - Time Differences between {min_val} and {max_val} minutes",
#     labels={'TimeDifferenceFormatted': 'Time Difference (MM:SS)', 'Count': 'Count'}
# )
# fig.update_xaxes(tickangle=-45)
# st.plotly_chart(fig, use_container_width=True)

# # --- Show Matching Programs ---
# if not agg_df.empty:
#     selected_time = st.selectbox("Select a Time Difference to view matching programs:", agg_df['TimeDifferenceFormatted'])
#     matched_programs = filtered_df[filtered_df['TimeDifferenceFormatted'] == selected_time]['Program'].unique()

#     st.subheader(f"Programs with Time Difference {selected_time}")
#     if len(matched_programs) == 0:
#         st.info("No matching programs found.")
#     else:
#         st.write(pd.DataFrame(matched_programs, columns=["Program"]))
# else:
#     st.warning("No data matches the selected filters.")


# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from datetime import datetime

# st.set_page_config(page_title="Time Difference Explorer", layout="wide")
# st.title("📺 Time Difference Explorer")

# # --- Dataset Selection ---
# dataset_option = st.selectbox("Choose Dataset", ["WDSU", "WBAL", "WBAL - Part2"])

# if dataset_option == "WDSU":
#     file_path = "WDSU.xlsx"
# elif dataset_option == "WBAL":
#     file_path = "WBAL.xlsx"
# else:
#     file_path = "WBAL - Part2.xlsx"

# # --- Load and Clean Data ---
# df = pd.read_excel(file_path)
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

# if 'Air Date' in df.columns:
#     df['AirDateOnly'] = pd.to_datetime(df['Air Date'], errors='coerce').dt.date
#     df = df.dropna(subset=['AirDateOnly'])
#     df['DayName'] = pd.to_datetime(df['AirDateOnly']).dt.day_name()
# else:
#     df['AirDateOnly'] = None
#     df['DayName'] = None

# # --- Time Range Slider ---
# min_val, max_val = st.slider(
#     "Select Time Difference Range (minutes)",
#     0, int(df['TimeInSeconds'].max() // 60) + 1,
#     (0, int(df['TimeInSeconds'].max() // 60) + 1),
#     step=1
# )
# min_sec = min_val * 60
# max_sec = max_val * 60

# # --- Program Filter ---
# all_programs = sorted(df['Program'].unique())
# with st.expander("🎛️ Program Filter"):
#     select_all_programs = st.checkbox("Select All Programs", value=True)
#     if select_all_programs:
#         selected_programs = st.multiselect(
#             "Choose programs to include (one below the other):",
#             options=all_programs,
#             default=all_programs,
#             label_visibility="visible"
#         )
#     else:
#         selected_programs = st.multiselect(
#             "Choose programs to include (one below the other):",
#             options=all_programs,
#             label_visibility="visible"
#         )

# # --- Bidirectional Air Date and Day Filters Setup ---

# if df['AirDateOnly'].notnull().any():

#     # All unique Air Dates and Days
#     all_dates = sorted(df['AirDateOnly'].unique())
#     all_days = sorted(df['DayName'].dropna().unique())

#     # Initialize session state for selections if not exist
#     if 'selected_days' not in st.session_state:
#         st.session_state.selected_days = all_days.copy()
#     if 'selected_dates' not in st.session_state:
#         st.session_state.selected_dates = all_dates.copy()

#     # Functions to update each filter when the other changes
#     def on_days_change():
#         # Filter dates based on selected days
#         filtered_dates = sorted(df[df['DayName'].isin(st.session_state.selected_days)]['AirDateOnly'].unique())
#         st.session_state.selected_dates = [d for d in st.session_state.selected_dates if d in filtered_dates]
#         # If no dates left, reset to all filtered dates
#         if not st.session_state.selected_dates:
#             st.session_state.selected_dates = filtered_dates

#     def on_dates_change():
#         # Filter days based on selected dates
#         filtered_days = sorted(df[df['AirDateOnly'].isin(st.session_state.selected_dates)]['DayName'].unique())
#         st.session_state.selected_days = [d for d in st.session_state.selected_days if d in filtered_days]
#         # If no days left, reset to all filtered days
#         if not st.session_state.selected_days:
#             st.session_state.selected_days = filtered_days

#     # Day Name Filter with callback
#     selected_days = st.multiselect(
#         "Select Days to include:",
#         options=all_days,
#         default=st.session_state.selected_days,
#         key='selected_days',
#         on_change=on_days_change
#     )

#     # Air Date Filter with callback
#     # Show only dates matching selected days
#     available_dates = sorted(df[df['DayName'].isin(st.session_state.selected_days)]['AirDateOnly'].unique())
#     # Reset selected_dates if it contains dates not in available_dates
#     st.session_state.selected_dates = [d for d in st.session_state.selected_dates if d in available_dates]
#     if not st.session_state.selected_dates:
#         st.session_state.selected_dates = available_dates

#     selected_dates = st.multiselect(
#         "Select Air Dates to include:",
#         options=available_dates,
#         default=st.session_state.selected_dates,
#         key='selected_dates',
#         on_change=on_dates_change
#     )

# else:
#     selected_dates = None
#     selected_days = None

# # --- Sorting Options ---
# col1, col2 = st.columns(2)
# with col1:
#     sort_column = st.radio("Sort by:", options=["Time Difference", "Count"], index=1)
# with col2:
#     sort_order = st.radio("Sort Order:", options=["Descending", "Ascending"])
# ascending = sort_order == "Ascending"

# # --- Apply Filters ---
# filtered_df = df[
#     (df['TimeInSeconds'] >= min_sec) &
#     (df['TimeInSeconds'] <= max_sec) &
#     (df['Program'].isin(selected_programs))
# ]

# if selected_dates is not None:
#     filtered_df = filtered_df[filtered_df['AirDateOnly'].isin(selected_dates)]

# if selected_days is not None:
#     filtered_df = filtered_df[filtered_df['DayName'].isin(selected_days)]

# # --- Aggregate for Chart ---
# agg_df = filtered_df.groupby('TimeDifferenceFormatted').size().reset_index(name='Count')

# if sort_column == "Count":
#     agg_df = agg_df.sort_values(by='Count', ascending=ascending)
# else:
#     agg_df['Seconds'] = agg_df['TimeDifferenceFormatted'].apply(
#         lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])
#     )
#     agg_df = agg_df.sort_values(by='Seconds', ascending=ascending)

# # --- Plot ---
# fig = px.bar(
#     agg_df,
#     x='TimeDifferenceFormatted',
#     y='Count',
#     title=f"{dataset_option} - Time Differences between {min_val} and {max_val} minutes",
#     labels={'TimeDifferenceFormatted': 'Time Difference (MM:SS)', 'Count': 'Count'}
# )
# fig.update_xaxes(tickangle=-45)
# st.plotly_chart(fig, use_container_width=True)

# # --- Show Matching Programs ---
# if not agg_df.empty:
#     selected_time = st.selectbox("Select a Time Difference to view matching programs:", agg_df['TimeDifferenceFormatted'])
#     matched_programs = filtered_df[filtered_df['TimeDifferenceFormatted'] == selected_time]['Program'].unique()

#     st.subheader(f"Programs with Time Difference {selected_time}")
#     if len(matched_programs) == 0:
#         st.info("No matching programs found.")
#     else:
#         st.write(pd.DataFrame(matched_programs, columns=["Program"]))
# else:
#     st.warning("No data matches the selected filters.")




#works perfectly fine and now below adding the ALL filters to all:


import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Time Difference Explorer", layout="wide")
st.title("📺 Time Difference Explorer")

# --- Dataset Selection ---
dataset_option = st.selectbox("Choose Dataset", ["WDSU", "WBAL", "WBAL_2"])

if dataset_option == "WDSU":
    file_path = "WDSU.xlsx"
elif dataset_option == "WBAL":
    file_path = "WBAL.xlsx"
elif dataset_option == "WBAL_2":
    file_path = "WBAL_2.xlsx"
else:
    st.error("Unknown dataset selected. Please choose a valid option.")
    st.stop()

# --- Load and Clean Data ---
df = pd.read_excel(file_path)
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

if 'Air Date' in df.columns:
    df['AirDateOnly'] = pd.to_datetime(df['Air Date'], errors='coerce').dt.date
    df = df.dropna(subset=['AirDateOnly'])
    df['DayName'] = pd.to_datetime(df['AirDateOnly']).dt.day_name()
else:
    df['AirDateOnly'] = None
    df['DayName'] = None

# --- Bidirectional Air Date and Day Filters Setup ---

if df['AirDateOnly'].notnull().any():

    # All unique Air Dates and Days
    all_dates = sorted(df['AirDateOnly'].unique())
    all_days = sorted(df['DayName'].dropna().unique())

    # Initialize session state for selections if not exist
    if 'selected_days' not in st.session_state:
        st.session_state.selected_days = all_days.copy()
    if 'selected_dates' not in st.session_state:
        st.session_state.selected_dates = all_dates.copy()

    # Functions to update each filter when the other changes
    def on_days_change():
        filtered_dates = sorted(df[df['DayName'].isin(st.session_state.selected_days)]['AirDateOnly'].unique())
        st.session_state.selected_dates = [d for d in st.session_state.selected_dates if d in filtered_dates]
        if not st.session_state.selected_dates:
            st.session_state.selected_dates = filtered_dates

    def on_dates_change():
        filtered_days = sorted(df[df['AirDateOnly'].isin(st.session_state.selected_dates)]['DayName'].unique())
        st.session_state.selected_days = [d for d in st.session_state.selected_days if d in filtered_days]
        if not st.session_state.selected_days:
            st.session_state.selected_days = filtered_days

    # Day Name Filter with callback
    selected_days = st.multiselect(
        "Select Days to include:",
        options=all_days,
        default=st.session_state.selected_days,
        key='selected_days',
        on_change=on_days_change
    )

    # Air Date Filter with callback
    available_dates = sorted(df[df['DayName'].isin(st.session_state.selected_days)]['AirDateOnly'].unique())
    st.session_state.selected_dates = [d for d in st.session_state.selected_dates if d in available_dates]
    if not st.session_state.selected_dates:
        st.session_state.selected_dates = available_dates

    selected_dates = st.multiselect(
        "Select Air Dates to include:",
        options=available_dates,
        default=st.session_state.selected_dates,
        key='selected_dates',
        on_change=on_dates_change
    )

else:
    selected_dates = None
    selected_days = None

# --- Apply Day and Date Filters early ---
df_filtered_days_dates = df.copy()
if selected_dates is not None:
    df_filtered_days_dates = df_filtered_days_dates[df_filtered_days_dates['AirDateOnly'].isin(selected_dates)]
if selected_days is not None:
    df_filtered_days_dates = df_filtered_days_dates[df_filtered_days_dates['DayName'].isin(selected_days)]

# --- Program Filter based on filtered days/dates ---
all_programs = sorted(df_filtered_days_dates['Program'].unique())
with st.expander("🎛️ Program Filter"):
    select_all_programs = st.checkbox("Select All Programs", value=True, key="select_all_programs")
    if select_all_programs:
        selected_programs = st.multiselect(
            "Choose programs to include (one below the other):",
            options=all_programs,
            default=all_programs,
            label_visibility="visible",
            key="program_multiselect"
        )
    else:
        selected_programs = st.multiselect(
            "Choose programs to include (one below the other):",
            options=all_programs,
            label_visibility="visible",
            key="program_multiselect"
        )

# --- Filter by selected programs ---
df_filtered_prog = df_filtered_days_dates[df_filtered_days_dates['Program'].isin(selected_programs)]

# --- Time Range Slider based on filtered programs ---
min_possible = 0
max_possible = int(df_filtered_prog['TimeInSeconds'].max() // 60) + 1 if not df_filtered_prog.empty else 1

min_val, max_val = st.slider(
    "Select Time Difference Range (minutes)",
    min_possible, max_possible,
    (min_possible, max_possible),
    step=1,
    key="time_diff_slider"
)
min_sec = min_val * 60
max_sec = max_val * 60

# --- Now apply all filters to original df ---
filtered_df = df_filtered_prog[
    (df_filtered_prog['TimeInSeconds'] >= min_sec) & 
    (df_filtered_prog['TimeInSeconds'] <= max_sec)
]

# --- Sorting Options ---
col1, col2 = st.columns(2)
with col1:
    sort_column = st.radio("Sort by:", options=["Time Difference", "Count"], index=1)
with col2:
    sort_order = st.radio("Sort Order:", options=["Descending", "Ascending"])
ascending = sort_order == "Ascending"

# --- Aggregate for Chart ---
agg_df = filtered_df.groupby('TimeDifferenceFormatted').size().reset_index(name='Count')

if sort_column == "Count":
    agg_df = agg_df.sort_values(by='Count', ascending=ascending)
else:
    agg_df['Seconds'] = agg_df['TimeDifferenceFormatted'].apply(
        lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1])
    )
    agg_df = agg_df.sort_values(by='Seconds', ascending=ascending)

# --- Plot ---
fig = px.bar(
    agg_df,
    x='TimeDifferenceFormatted',
    y='Count',
    title=f"{dataset_option} - Time Differences between {min_val} and {max_val} minutes",
    labels={'TimeDifferenceFormatted': 'Time Difference (MM:SS)', 'Count': 'Count'}
)
fig.update_xaxes(tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# --- Show Matching Programs ---
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

