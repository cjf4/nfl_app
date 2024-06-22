import streamlit as st
import pandas as pd
import duckdb
import os

import altair as alt

relative_path = 'data/front_end_data/parquet_files/qb_epa.parquet'
abs_path = os.path.abspath(relative_path)
df = pd.read_parquet(abs_path)

st.title('Fenton NFL Analysis')
st.write("Chris Fenton's NFL Analysis")


qb_selection = st.selectbox(
    "QB",
    ("J.Allen","J.Hurts"))

season_selection = st.selectbox(
    "Season",
    (2023, 2022, 2021))

filtered_data = df[df.qb_name==qb_selection].sort_values(by='week')

color_scale = alt.Scale(
    domain=['win', 'loss', 'tie'],
    range=['#53b874', '#cc503f', '#d3d3d3']  
)

chart = alt.Chart(filtered_data).mark_bar(filled=True).encode(
    x=alt.X('week_opponent'
                , sort=alt.EncodingSortField(field='week')
            )
    , y=alt.Y('avg_epa',scale=alt.Scale(domain=[-1, 1]))
    
    , color=alt.Color('game_result', scale=color_scale)
    , tooltip=['opponent']  
)

st.altair_chart(chart, use_container_width=True)  

all_qb_chart = alt.Chart(df).mark_bar().encode(
    alt.X('avg_epa',bin=alt.Bin(maxbins=30))
    , y='count()'
)

st.altair_chart(all_qb_chart,use_container_width=True)
#st.altair_chart(chart)


st.write(filtered_data)

