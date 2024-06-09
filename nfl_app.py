import streamlit as st
import pandas as pd
import duckdb

con = duckdb.connect(database = "nflfastr/nflfastR_db.duckdb"
                     , read_only = True)

first_down_query = """
with cte as (
	SELECT 
	pass == 1 AS pass_play
	, season
	, week
	, posteam as team
	, count(posteam) AS plays
	, mean(epa) AS avg_epa
	, plays * avg_epa AS total_epa
	
FROM MAIN.PBP_DATA 
WHERE 1=1
	AND down = 1
	AND ydstogo = 10
	AND half_seconds_remaining > 120
	AND ((wp > 0.1) AND (wp < .9))
	AND NOT (play_type = 'no_play')
GROUP BY 1,2,3,4


)



, agg as (
select 
  team
  , week
  , season
  , sum(case when pass_play then plays else 0 end) as pass_plays
  , sum(plays) as total_plays
  , total_plays - pass_plays as run_plays
  , pass_plays / total_plays as first_down_pass_rate
  , sum(total_epa) as total_epa
  , sum(case when pass_play then total_epa else 0 end) as pass_play_epa
  , sum(case when not pass_play then total_epa else 0 end) as run_play_epa
FROM cte
where 1=1


group by 1,2,3
order by 1
)

select * 
, total_epa / total_plays as first_down_epa
, run_play_epa / run_plays as run_play_epa
, pass_play_epa / pass_plays as pass_play_epa
from agg
order by season desc, team, week

"""


df = con.execute(first_down_query).df()

option = st.selectbox(
    "Team",
    ("ARI", "BUF", "GB"))

st.write("First NFL App")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))
st.write(df[df.team==option])