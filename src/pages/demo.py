import streamlit as st
import sys
from pathlib import Path
import time
from datetime import time
from datetime import datetime
import pandas as pd
from st_aggrid import AgGrid
import altair as alt
from st_aggrid import AgGrid, GridOptionsBuilder 
import plotly.graph_objects as go
import plotly.express as px

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from rsc.config import config_params

data_dir = config_params.data_dir

@st.cache_data
def load_data():
    df = pd.read_csv(f"{data_dir}/season2425.csv", sep = ';')
    return df

df_raw = load_data()

@st.cache_resource()
def preprocess_dataframe_results(df_raw):
    df = df_raw.copy()
    
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
    df = df.sort_values(by = 'Data', ascending = False)
    df['Perc Placcaggi Avanzanti'] = (df['Placcaggi Avanzanti'] / df['Placcaggi Tentati'] * 100).astype(int)
    df['Perc Placcaggi Non Avanzanti'] = (df['Placcaggi Non Avanzanti'] / df['Placcaggi Tentati'] * 100).astype(int)
    df['Perc Placcaggi Mancati'] = (df['Placcaggi Mancati'] / df['Placcaggi Tentati'] * 100).astype(int)
    
    df['Perc Portatori Dominanti'] = (df['Portatori Dominanti'] / df['Numero Portatori'] * 100).astype(int)
    df['Perc Portatori Avanzanti'] = (df['Portatori Avanzanti'] / df['Numero Portatori'] * 100).astype(int)
    df['Perc Portatori Non Avanzanti'] = (df['Portatori Non Avanzanti'] / df['Numero Portatori'] * 100).astype(int)
    
    return df
df = preprocess_dataframe_results(df_raw)

st.title("Demo Data Analysis Cus Torino Rugby")

st.header("Statistiche Squadra")
AgGrid(df, height = 200, editable = False, width = '100%')


st.divider()

st.header("Data Visualization")

tabs1, tabs2 = st.tabs(['Game Analysis', 'Historical Analysis'])

with tabs1:
    st.header("Game Analysis")

    opponents = df.sort_values(by = 'Data', ascending = False)['Avversario'].unique().tolist()
    selected_opponent = st.selectbox("Select Opponent", opponents)

    df_opponent = df[df['Avversario'] == selected_opponent]

    st.subheader("Possession and Territory")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = go.Figure(data=[
            go.Pie(labels=["Possesso CUS Torino", f"Possesso {selected_opponent}"], 
                values=[df_opponent['Possesso CUS Torino'].values[0], 100 - df_opponent['Possesso CUS Torino'].values[0]], 
                hole=0.3, 
                textinfo='label+percent', 
                title="Possesso",
                marker=dict(colors=["#2279AB", "#e35c2b"])),
                
        ])
        fig1.update_layout(grid=dict(rows=1, columns=1), showlegend=True)
        st.plotly_chart(fig1)
    with col2:
        fig2 = go.Figure(data=[
            go.Pie(labels=["Territorio CUS Torino", f"Territorio {selected_opponent}"], 
                values=[df_opponent['Territorio CUS Torino'].values[0], 100 - df_opponent['Territorio CUS Torino'].values[0]], 
                hole=0.3, 
                textinfo='label+percent', 
                title="Territorio",
                marker=dict(colors=["#2279AB", "#e35c2b"])),
                
        ])
        fig2.update_layout(grid=dict(rows=1, columns=1), showlegend=True)
        st.plotly_chart(fig2)

    # # Visualization 2: Tackling Efficiency
    # Data preparation for Tackling Efficiency
    tackling_data = {
        "Tipo Placcaggio": ["Placcaggi Avanzanti", "Placcaggi Non Avanzanti", "Placcaggi Mancati", "Placcaggi Cover"],
        "Count": [
            df_opponent["Placcaggi Avanzanti"].values[0],
            df_opponent["Placcaggi Non Avanzanti"].values[0],
            df_opponent["Placcaggi Mancati"].values[0],
            df_opponent["Placcaggi Cover"].values[0]
        ]
    }   

    # Calculate percentages
    total_tackles = sum(tackling_data["Count"])
    tackling_data["Percentage"] = [round((count / total_tackles) * 100, 2) for count in tackling_data["Count"]]
    tackling_data["Percentage"] = [f"{percentage}%" for percentage in tackling_data["Percentage"]]

    # Create a DataFrame for the bar chart
    tackling_df = pd.DataFrame(tackling_data)

    # Plot the bar chart
    st.subheader("Efficienza Placcaggio")
    fig3 = px.bar(
        tackling_df,
        x="Tipo Placcaggio",
        y="Count",
        labels={"x": "Tipo Placcaggio", "y": "Count"},
        text="Percentage",  # This adds the percentage as text over the bars (optional)
        hover_data={"Percentage": True},  # Include percentage in the tooltip
        title=f"Placcaggi (Totali: {total_tackles})",
        color_discrete_sequence=["#2279AB"],
    )
    st.plotly_chart(fig3)

    # Visualization 3: Offensive Metrics
    st.subheader("Statistiche Offensive")
    col1, col2, col3 = st.columns(3)

    # Plot 1: Portatori
    with col1:
        # Prepare data for Portatori
        portatori_data = {
            "Tipo": ["Dominanti", "Avanzanti", "Non Avanzanti"],
            "Count": [
                df_opponent['Portatori Dominanti'].values[0],
                df_opponent['Portatori Avanzanti'].values[0],
                df_opponent['Portatori Non Avanzanti'].values[0]
            ],
        }

        # Convert data to DataFrame
        portatori_df = pd.DataFrame(portatori_data)

        # Calculate percentage
        total_portatori = portatori_df["Count"].sum()
        portatori_df["Percentage"] = (
            (portatori_df["Count"] / total_portatori) * 100
        ).round(2)
        portatori_df["Percentage"] = portatori_df["Percentage"].astype(str) + "%"

        # Create the bar chart with Plotly Express
        fig_portatori = px.bar(
            portatori_df,
            x="Tipo",
            y="Count",
            text="Percentage",  # Add percentages as text over the bars
            hover_data={"Percentage": True},  # Show percentages in the tooltip
            title=f"Portatori (Totali: {total_portatori})",
            labels={"Tipo": "Tipo", "Count": "Count"},
            color_discrete_sequence=["#2279AB"],
        )

        # Update layout
        fig_portatori.update_layout(
            yaxis_title="Count",
            xaxis_title="Tipo",
            barmode="group",
        )

        # Show the chart
        st.plotly_chart(fig_portatori, use_container_width=True)

    # Plot 2: Offloads
    with col2:
        offloads_data = {
            "Tipo": ["Offloads Positivi", "Offloads Negativi"],
            "Count": [df_opponent["Offload Positivi"].values[0], df_opponent["Offload Negativi"].values[0]],
        }

        offloads_df = pd.DataFrame(offloads_data)

        total_offloads = offloads_df["Count"].sum()
        offloads_df["Percentage"] = (
            (offloads_df["Count"] / total_offloads) * 100
        ).round(2)
        offloads_df["Percentage"] = offloads_df["Percentage"].astype(str) + "%"

        fig_offloads = px.bar(
            offloads_df,
            x="Tipo",
            y="Count",
            text="Percentage",
            hover_data={"Percentage": True},
            title=f"Offloads (Totali: {total_offloads})",
            labels={"Tipo": "Tipo", "Count": "Count"},
            color_discrete_sequence=["#deb368"],
        )

        fig_offloads.update_layout(
            yaxis_title="Count",
            xaxis_title="Tipo",
            barmode="group",
        )

        st.plotly_chart(fig_offloads, use_container_width=True)
        

    # Plot 3: Kicks in Play
    with col3:
        kicks_data = {
            "Tipo": ["Kicks Positivo", "Kicks Negativo"],
            "Count": [df_opponent["Kicks Positivo"].values[0], df_opponent["Kicks Negativo"].values[0]],
        }

        kicks_df = pd.DataFrame(kicks_data)

        total_kicks = kicks_df["Count"].sum()
        kicks_df["Percentage"] = (
            (kicks_df["Count"] / total_kicks) * 100
        ).round(2)
        kicks_df["Percentage"] = kicks_df["Percentage"].astype(str) + "%"

        fig_kicks = px.bar(
            kicks_df,
            x="Tipo",
            y="Count",
            text="Percentage",
            hover_data={"Percentage": True},
            title=f"Kicks (Totali: {total_kicks})",
            labels={"Tipo": "Tipo", "Count": "Count"},
            color_discrete_sequence=["#8ede68"],
        )

        fig_kicks.update_layout(
            yaxis_title="Count",
            xaxis_title="Tipo",
            barmode="group",
        )

        st.plotly_chart(fig_kicks, use_container_width=True)

    st.divider()

    st.subheader("Metriche")
    st.text("Displaying some metrics for the Team Stats dataset. The comparison is made against the average of all games played, game selected included.")

    tries_scored_avg_all = df["Mete CUS Torino"].mean()
    tries_conceded_avg_all = df["Mete Avversario"].mean()
    penalty_off_avg_all = df["Falli Offensivi"].mean()
    penalty_def_avg_all = df["Falli Difensivi"].mean()
    avg_dominant_tackles_per_game_all = df["Placcaggi Avanzanti"].mean()
    avg_not_dominant_tackles_per_game_all = df["Placcaggi Non Avanzanti"].mean()
    avg_missed_tackles_per_game_all = df["Placcaggi Mancati"].mean()
    avg_cover_tackles_per_game_all = df["Placcaggi Cover"].mean()
    avg_defensor_beaten_per_game_all = df["Difensori Battuti"].mean()
    avg_portatori_dominanti_per_game_all = df["Portatori Dominanti"].mean()
    avg_portatori_avanzanti_per_game_all = df["Portatori Avanzanti"].mean()
    avg_portatori_non_avanzanti_per_game_all = df["Portatori Non Avanzanti"].mean()


    tries_scored_selected_game = df_opponent["Mete CUS Torino"].values[0]
    tries_conceded_selected_game = df_opponent["Mete Avversario"].values[0]
    penalty_off_selected_game = df_opponent["Falli Offensivi"].values[0]
    penalty_def_selected_game = df_opponent["Falli Difensivi"].values[0]
    avg_dominant_tackles_per_game = df_opponent["Placcaggi Avanzanti"].values[0]
    avg_not_dominant_tackles_per_game = df_opponent["Placcaggi Non Avanzanti"].values[0]
    avg_missed_tackles_per_game = df_opponent["Placcaggi Mancati"].values[0]
    avg_cover_tackles_per_game = df_opponent["Placcaggi Cover"].values[0]
    avg_defensor_beaten_per_game = df_opponent["Difensori Battuti"].values[0]
    avg_portatori_dominanti_per_game = df_opponent["Portatori Dominanti"].values[0]
    avg_portatori_avanzanti_per_game = df_opponent["Portatori Avanzanti"].values[0]
    avg_portatori_non_avanzanti_per_game = df_opponent["Portatori Non Avanzanti"].values[0]

    columns = st.columns(4)
    columns[0].metric(label="Mete CUS Torino", value=f"{tries_scored_selected_game:.2f}", delta = f"{tries_scored_selected_game - tries_scored_avg_all:.2f}")
    columns[1].metric(label=f"Mete {selected_opponent}", value=f"{tries_conceded_selected_game:.2f}", delta=f"{tries_conceded_selected_game - tries_conceded_avg_all:.2f}", delta_color="inverse")
    columns[2].metric(label="Falli Offensivi", value=f"{penalty_off_selected_game:.2f}", delta = f"{penalty_off_selected_game - penalty_off_avg_all:.2f}", delta_color="inverse")
    columns[3].metric(label="Falli Difensivi", value=f"{penalty_def_selected_game:.2f}", delta = f"{penalty_def_selected_game - penalty_def_avg_all:.2f}", delta_color="inverse")

    columns = st.columns(4)
    columns[0].metric(label="Placcaggi Dominanti", value=f"{avg_dominant_tackles_per_game:.2f}", delta = f"{avg_dominant_tackles_per_game - avg_dominant_tackles_per_game_all:.2f}")
    columns[1].metric(label="Placcaggi Non Dominanti", value=f"{avg_not_dominant_tackles_per_game:.2f}", delta = f"{avg_not_dominant_tackles_per_game - avg_not_dominant_tackles_per_game_all:.2f}", delta_color="off")
    columns[2].metric(label="Placcaggi Mancati", value=f"{avg_missed_tackles_per_game:.2f}", delta = f"{avg_missed_tackles_per_game - avg_missed_tackles_per_game_all:.2f}", delta_color="inverse")
    columns[3].metric(label="Placcaggi Cover", value=f"{avg_cover_tackles_per_game:.2f}", delta = f"{avg_cover_tackles_per_game - avg_cover_tackles_per_game_all:.2f}", delta_color="off")

    columns = st.columns(4)
    columns[0].metric(label="Difensori Battuti", value=f"{avg_defensor_beaten_per_game:.2f}", delta = f"{avg_defensor_beaten_per_game - avg_defensor_beaten_per_game_all:.2f}")
    columns[1].metric(label="Portatori Dominanti", value=f"{avg_portatori_dominanti_per_game:.2f}", delta = f"{avg_portatori_dominanti_per_game - avg_portatori_dominanti_per_game_all:.2f}")
    columns[2].metric(label="Portatori Avanzanti", value=f"{avg_portatori_avanzanti_per_game:.2f}", delta = f"{avg_portatori_avanzanti_per_game - avg_portatori_avanzanti_per_game_all:.2f}")
    columns[3].metric(label="Portatori Non Avanzanti", value=f"{avg_portatori_non_avanzanti_per_game:.2f}", delta = f"{avg_portatori_non_avanzanti_per_game - avg_portatori_non_avanzanti_per_game_all:.2f}")
with tabs2:
    st.header("Historical Data")
    st.write("Historical data for the team")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Penalties")
        point_selector = alt.selection_point("point_selection")
        chart = (
            alt.Chart(df)
            .mark_point()
            .encode(
                x="Falli Offensivi",
                y="Falli Difensivi",
                color="Risultato",
                tooltip=["Falli Offensivi", "Falli Difensivi", "Risultato", "Avversario"],
                fillOpacity=alt.condition(point_selector, alt.value(1), alt.value(0.3)),
            )
            .add_params(point_selector)
        )

        event = st.altair_chart(chart, key="penalties", on_select="rerun")

        if len(event['selection']['point_selection']) == 0:
            pass
        else:
            point_selected_penalty_off = event['selection']['point_selection'][0]['Falli Offensivi']
            point_selected_penalty_def = event['selection']['point_selection'][0]['Falli Difensivi']
            point_selected_opponent = event['selection']['point_selection'][0]['Risultato']

            game_selected = df[(df['Falli Offensivi'] == point_selected_penalty_off) 
                            & (df['Falli Difensivi'] == point_selected_penalty_def) 
                            & (df['Risultato'] == point_selected_opponent)]

            st.dataframe(game_selected)

    with col2:
        

        st.subheader("Tackles")
        point_selector = alt.selection_point("point_selection")

        chart_tackles = (
            alt.Chart(df)
            .mark_point()
            .encode(
                x="Perc Placcaggi Avanzanti",
                y="Perc Placcaggi Non Avanzanti",
                color="Risultato",
                tooltip=["Perc Placcaggi Avanzanti", "Perc Placcaggi Non Avanzanti", "Risultato", "Avversario"],
                fillOpacity=alt.condition(point_selector, alt.value(1), alt.value(0.3)),
            )
            .add_params(point_selector)
        )
        event_tackles = st.altair_chart(chart_tackles, key="tackles", on_select="rerun")

        if len(event_tackles['selection']['point_selection']) == 0:
            pass
        else:
            point_selected_penalty_off = event_tackles['selection']['point_selection'][0]['Perc Placcaggi Avanzanti']
            point_selected_penalty_def = event_tackles['selection']['point_selection'][0]['Perc Placcaggi Non Avanzanti']
            point_selected_opponent = event_tackles['selection']['point_selection'][0]['Risultato']

            game_selected = df[(df['Perc Placcaggi Avanzanti'] == point_selected_penalty_off) 
                            & (df['Perc Placcaggi Non Avanzanti'] == point_selected_penalty_def) 
                            & (df['Risultato'] == point_selected_opponent)]

            st.dataframe(game_selected)

st.header("Historical Analysis")
st.write("Historical analysis of the team")
selected_feature = st.selectbox("Select Feature", ["Possesso CUS Torino", 
                                                   "Territorio CUS Torino", 
                                                   "Falli Concessi",
                                                   "Placcaggi Totali",
                                                   "Portatori Totali",
                                                   "Tempo Effettivo"], index=0)
                                                   
df['Falli Concessi'] = df['Falli Difensivi'] + df['Falli Offensivi']
df['Placcaggi Totali'] = df['Placcaggi Avanzanti'] + df['Placcaggi Non Avanzanti'] + df['Placcaggi Mancati'] + df['Placcaggi Cover']
df['Portatori Totali'] = df['Portatori Dominanti'] + df['Portatori Avanzanti'] + df['Portatori Non Avanzanti']
basic_tooltip_features = ["Data", "Risultato", "Avversario"]
if selected_feature == "Placcaggi Totali":
    selected_feature_tooltip_features = [selected_feature, "Placcaggi Avanzanti", "Placcaggi Non Avanzanti", "Placcaggi Mancati", "Placcaggi Cover"]
elif selected_feature == "Portatori Totali":
    selected_feature_tooltip_features = [selected_feature, "Portatori Dominanti", "Portatori Avanzanti", "Portatori Non Avanzanti"]
else:
    selected_feature_tooltip_features = [selected_feature]
tooltip_features = basic_tooltip_features + selected_feature_tooltip_features

chart_hist_penalties = (alt.Chart(df)
                        .mark_line()
                        .encode(x='Data', y=selected_feature, 
                                tooltip=tooltip_features,
                                )
                        .properties(width=800, height=400)
                        )
chart_hist_penalties = chart_hist_penalties + chart_hist_penalties.mark_circle().encode(size=alt.value(200), color='Risultato')
st.altair_chart(chart_hist_penalties, use_container_width=True)

st.header("Metrics")
st.write("Displaying some metrics for the Team Stats dataset:")

option_map = {
    0: "Vittoria",
    1: "Sconfitta",
    2: "Pareggio",
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
tries_scored_avg_all = df["Mete CUS Torino"].mean()
tries_conceded_avg_all = df["Mete Avversario"].mean()
penalty_off_avg_all = df["Falli Offensivi"].mean()
penalty_def_avg_all = df["Falli Difensivi"].mean()
avg_dominant_tackles_per_game_all = df["Perc Placcaggi Avanzanti"].sum() / len(df)
avg_not_dominant_tackles_per_game_all = df["Perc Placcaggi Non Avanzanti"].sum() / len(df)
avg_missed_tackles_per_game_all = df["Perc Placcaggi Mancati"].sum() / len(df)

if (len(selection) == 0) or ("All" in selection) or (['Vittoria', 'Sconfitta', 'Pareggio'] == selection):
    selection = ['Vittoria', 'Sconfitta', 'Pareggio']    

    columns = st.columns(4)
    columns[0].metric(label="Avg Mete CUS Torino", value=f"{tries_scored_avg_all:.2f}")
    columns[1].metric(label="Avg Mete Avversario", value=f"{tries_conceded_avg_all:.2f}")
    columns[2].metric(label="Avg Falli Offensivi", value=f"{penalty_off_avg_all:.2f}")
    columns[3].metric(label="Avg Falli Difensivi", value=f"{penalty_def_avg_all:.2f}")
    columns = st.columns(3)
    columns[0].metric(label="Avg Placcaggi Avanzanti per Game", value=f"{avg_dominant_tackles_per_game_all:.2f}")
    columns[1].metric(label="Avg Placcaggi Non Avanzanti per Game", value=f"{avg_not_dominant_tackles_per_game_all:.2f}")
    columns[2].metric(label="Avg Missed Tackles per Game", value=f"{avg_missed_tackles_per_game_all:.2f}")

else:
    df_filtered = df.copy()
    if len(df_filtered) == 0:
        st.write("No data available for the selected filter")
    else:
        df_filtered = df_filtered[df_filtered['Risultato'].isin(selection)]

        tries_scored_avg = df_filtered["Mete CUS Torino"].mean()
        tries_conceded_avg = df_filtered["Mete Avversario"].mean()
        penalty_off_avg = df_filtered["Falli Offensivi"].mean()
        penalty_def_avg = df_filtered["Falli Difensivi"].mean()
        avg_dominant_tackles_per_game = df_filtered["Perc Placcaggi Avanzanti"].sum() / len(df_filtered)
        avg_not_dominant_tackles_per_game = df_filtered["Perc Placcaggi Non Avanzanti"].sum() / len(df_filtered)
        avg_missed_tackles_per_game = df_filtered["Perc Placcaggi Mancati"].sum() / len(df_filtered)

        columns = st.columns(4)
        columns[0].metric(label="Avg Mete CUS Torino", value=f"{tries_scored_avg:.2f}", delta = f"{tries_scored_avg - tries_scored_avg_all:.2f}")
        columns[1].metric(label="Avg Mete Avversario", value=f"{tries_conceded_avg:.2f}", delta=f"{tries_conceded_avg - tries_conceded_avg_all:.2f}", delta_color="inverse")
        columns[2].metric(label="Avg Falli Offensivi", value=f"{penalty_off_avg:.2f}", delta = f"{penalty_off_avg - penalty_off_avg_all:.2f}", delta_color="inverse")
        columns[3].metric(label="Avg Falli Difensivi", value=f"{penalty_def_avg:.2f}", delta = f"{penalty_def_avg - penalty_def_avg_all:.2f}", delta_color="inverse")
        columns = st.columns(3)
        columns[0].metric(label="Avg Placcaggi Avanzanti per Game", value=f"{avg_dominant_tackles_per_game:.2f}", delta = f"{avg_dominant_tackles_per_game - avg_dominant_tackles_per_game_all:.2f}")
        columns[1].metric(label="Avg Placcaggi Non Avanzanti per Game", value=f"{avg_not_dominant_tackles_per_game:.2f}", delta = f"{avg_not_dominant_tackles_per_game - avg_not_dominant_tackles_per_game_all:.2f}")
        columns[2].metric(label="Avg Placcaggi Mancati per Game", value=f"{avg_missed_tackles_per_game:.2f}", delta = f"{avg_missed_tackles_per_game - avg_missed_tackles_per_game_all:.2f}", delta_color="inverse")

