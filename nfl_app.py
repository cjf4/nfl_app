import streamlit as st
import pandas as pd
import duckdb

df = pd.read_parquet('data/front_end_data/first_down.parquet')


st.write("Chris Fenton's NFL Analysis")


team_selection = st.selectbox(
    "Team",
    ("ARI", "BUF", "GB"))

season_selection = st.selectbox(
    "Season",
    (2023, 2022, 2021))


st.write(df[(df.team==team_selection)
            & (df.season==season_selection)
            ])