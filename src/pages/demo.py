import streamlit as st
import sys
from pathlib import Path
import time
from datetime import time
from datetime import datetime
import pandas as pd
from st_aggrid import AgGrid
import altair as alt

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from rsc.config import config_params

data_dir = config_params.data_dir

@st.cache_data
def load_data():
    df = pd.read_csv(f"{data_dir}/team_stats_example.csv", sep = ';')
    return df

df_raw = load_data()

@st.cache_resource()
def preprocess_dataframe_results(df_raw):
    df = df_raw.copy()
    
    df['Date'] = pd.to_datetime(df['date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
    df = df.sort_values(by = 'Date', ascending = False)
    df['Results'] = df.apply(lambda x: 'Win' if x['score_cus_ft'] > x['score_opp_ft'] else 'Loss' if x['score_cus_ft'] < x['score_opp_ft'] else 'Draw', axis=1)
    df['Perc Dominant Tackles'] = (df['tackle_dom'] / df['tackle_attempt'] * 100).astype(int)
    df['Perc Not Dominant Tackles'] = (df['tackle_not_dom'] / df['tackle_attempt'] * 100).astype(int)
    df['Perc Missed Tackles'] = (df['tackle_miss'] / df['tackle_attempt'] * 100).astype(int)
    df = df.rename(columns = {
        'opponent': 'Opponent',
        'round' : 'Round',
        'try_scored' : 'Tries Scored',
        'try_conceded' : 'Tries Conceded',
        'penalty_off' : 'Penalty Off',
        'pen_dif' : 'Penalty Def',

    })
    df = df[['Date', 'Opponent', 'Round', 'Results', 
             'Tries Scored', 'Tries Conceded', 'Penalty Off', 'Penalty Def',
             'Perc Dominant Tackles', 'Perc Not Dominant Tackles', 'Perc Missed Tackles']]

    return df
df = preprocess_dataframe_results(df_raw)

st.title("Data Elements Showcase with Team Stats Example")

st.header("Results DataFrame Display")
AgGrid(df, height = 200, editable = False, width = '100%')

st.header("Plots DataFrame Display")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Penalties")
    point_selector = alt.selection_point("point_selection")
    chart = (
        alt.Chart(df)
        .mark_point()
        .encode(
            x="Penalty Off",
            y="Penalty Def",
            color="Results",
            tooltip=["Penalty Off", "Penalty Def", "Results", "Opponent"],
            fillOpacity=alt.condition(point_selector, alt.value(1), alt.value(0.3)),
        )
        .add_params(point_selector)
    )

    event = st.altair_chart(chart, key="penalties", on_select="rerun")

    if len(event['selection']['point_selection']) == 0:
        pass
    else:
        point_selected_penalty_off = event['selection']['point_selection'][0]['Penalty Off']
        point_selected_penalty_def = event['selection']['point_selection'][0]['Penalty Def']
        point_selected_opponent = event['selection']['point_selection'][0]['Results']

        game_selected = df[(df['Penalty Off'] == point_selected_penalty_off) 
                        & (df['Penalty Def'] == point_selected_penalty_def) 
                        & (df['Results'] == point_selected_opponent)]

        st.write(game_selected)

with col2:
    

    st.subheader("Tackles")
    point_selector = alt.selection_point("point_selection")

    chart_tackles = (
        alt.Chart(df)
        .mark_point()
        .encode(
            x="Perc Dominant Tackles",
            y="Perc Not Dominant Tackles",
            color="Results",
            tooltip=["Perc Dominant Tackles", "Perc Not Dominant Tackles", "Results", "Opponent"],
            fillOpacity=alt.condition(point_selector, alt.value(1), alt.value(0.3)),
        )
        .add_params(point_selector)
    )
    event_tackles = st.altair_chart(chart_tackles, key="tackles", on_select="rerun")

    if len(event_tackles['selection']['point_selection']) == 0:
        pass
    else:
        point_selected_penalty_off = event_tackles['selection']['point_selection'][0]['Perc Dominant Tackles']
        point_selected_penalty_def = event_tackles['selection']['point_selection'][0]['Perc Not Dominant Tackles']
        point_selected_opponent = event_tackles['selection']['point_selection'][0]['Results']

        game_selected = df[(df['Perc Dominant Tackles'] == point_selected_penalty_off) 
                        & (df['Perc Not Dominant Tackles'] == point_selected_penalty_def) 
                        & (df['Results'] == point_selected_opponent)]

        st.write(game_selected)

st.header("Historical Data")
df['Penalties Conceded'] = df['Penalty Def'] + df['Penalty Off']
chart_hist_penalties = (alt.Chart(df)
                        .mark_line()
                        .encode(x='Date', y='Penalties Conceded', 
                                tooltip=['Date', 'Penalties Conceded', "Results", "Opponent"],
                                )
                        .properties(width=800, height=400)
                        )
chart_hist_penalties = chart_hist_penalties + chart_hist_penalties.mark_circle().encode(size=alt.value(100))
st.altair_chart(chart_hist_penalties, use_container_width=True)

st.header("Metrics")
st.write("Displaying some metrics for the Team Stats dataset:")

option_map = {
    0: "Win",
    1: "Loss",
    2: "Draw",
    3: "All",
}
selection = st.segmented_control(
    "Filter by Results",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="multi",
    default=[3],
)

selection = [option_map[selection_value] for selection_value in selection]
tries_scored_avg_all = df["Tries Scored"].mean()
tries_conceded_avg_all = df["Tries Conceded"].mean()
penalty_off_avg_all = df["Penalty Off"].mean()
penalty_def_avg_all = df["Penalty Def"].mean()
avg_dominant_tackles_per_game_all = df["Perc Dominant Tackles"].sum() / len(df)
avg_not_dominant_tackles_per_game_all = df["Perc Not Dominant Tackles"].sum() / len(df)
avg_missed_tackles_per_game_all = df["Perc Missed Tackles"].sum() / len(df)

if (len(selection) == 0) or ("All" in selection) or (['Win', 'Loss', 'Draw'] == selection):
    selection = ['Win', 'Loss', 'Draw']    

    columns = st.columns(4)
    columns[0].metric(label="Avg Tries Scored", value=f"{tries_scored_avg_all:.2f}")
    columns[1].metric(label="Avg Tries Conceded", value=f"{tries_conceded_avg_all:.2f}")
    columns[2].metric(label="Avg Penalty Off", value=f"{penalty_off_avg_all:.2f}")
    columns[3].metric(label="Avg Penalty Def", value=f"{penalty_def_avg_all:.2f}")
    columns = st.columns(3)
    columns[0].metric(label="Avg Dominant Tackles per Game", value=f"{avg_dominant_tackles_per_game_all:.2f}")
    columns[1].metric(label="Avg Not Dominant Tackles per Game", value=f"{avg_not_dominant_tackles_per_game_all:.2f}")
    columns[2].metric(label="Avg Missed Tackles per Game", value=f"{avg_missed_tackles_per_game_all:.2f}")

else:
    df_filtered = df.copy()
    if len(df_filtered) == 0:
        st.write("No data available for the selected filter")
    else:
        df_filtered = df_filtered[df_filtered['Results'].isin(selection)]

        tries_scored_avg = df_filtered["Tries Scored"].mean()
        tries_conceded_avg = df_filtered["Tries Conceded"].mean()
        penalty_off_avg = df_filtered["Penalty Off"].mean()
        penalty_def_avg = df_filtered["Penalty Def"].mean()
        avg_dominant_tackles_per_game = df_filtered["Perc Dominant Tackles"].sum() / len(df_filtered)
        avg_not_dominant_tackles_per_game = df_filtered["Perc Not Dominant Tackles"].sum() / len(df_filtered)
        avg_missed_tackles_per_game = df_filtered["Perc Missed Tackles"].sum() / len(df_filtered)

        columns = st.columns(4)
        columns[0].metric(label="Avg Tries Scored", value=f"{tries_scored_avg:.2f}", delta = f"{tries_scored_avg - tries_scored_avg_all:.2f}")
        columns[1].metric(label="Avg Tries Conceded", value=f"{tries_conceded_avg:.2f}", delta=f"{tries_conceded_avg - tries_conceded_avg_all:.2f}", delta_color="inverse")
        columns[2].metric(label="Avg Penalty Off", value=f"{penalty_off_avg:.2f}", delta = f"{penalty_off_avg - penalty_off_avg_all:.2f}", delta_color="inverse")
        columns[3].metric(label="Avg Penalty Def", value=f"{penalty_def_avg:.2f}", delta = f"{penalty_def_avg - penalty_def_avg_all:.2f}", delta_color="inverse")
        columns = st.columns(3)
        columns[0].metric(label="Avg Dominant Tackles per Game", value=f"{avg_dominant_tackles_per_game:.2f}", delta = f"{avg_dominant_tackles_per_game - avg_dominant_tackles_per_game_all:.2f}")
        columns[1].metric(label="Avg Not Dominant Tackles per Game", value=f"{avg_not_dominant_tackles_per_game:.2f}", delta = f"{avg_not_dominant_tackles_per_game - avg_not_dominant_tackles_per_game_all:.2f}")
        columns[2].metric(label="Avg Missed Tackles per Game", value=f"{avg_missed_tackles_per_game:.2f}", delta = f"{avg_missed_tackles_per_game - avg_missed_tackles_per_game_all:.2f}", delta_color="inverse")

