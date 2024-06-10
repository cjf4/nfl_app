with 

qbs as (
	SELECT 
		passer_player_id as qb_id
		, count(*) as passes
	FROM 
		main.pbp_data
	
	WHERE 
		season =2023
	group by 1
		having passes >= 20
		
)

, plays as (

SELECT 
	passer_player_name 
	, passer_player_id 
	, rusher_player_name 
	, COALESCE(passer_player_name,rusher_player_name) as qb_name
	, play_type 
	, epa
	, week
	, posteam
	, defteam
	, score_differential 
	, down 
	, ydstogo 
	, yardline_100 
	, qb_dropback 
	, result
	, home_team = posteam as is_home
	, case 
		when result = 0 then 'tie'
		when (is_home and result > 0)
				or (not is_home and result < 0)
			then 'win'
		else 'loss' end as game_result
FROM 
	main.pbp_data 
	join qbs
		on (qbs.qb_id = passer_player_id 
				or qbs.qb_id = rusher_player_id )
WHERE 
	season = 2023
--	 and (passer_player_id = '00-0034857'
--	 		or rusher_player_id ='00-0034857')
)
--select * from plays
select
	week
	, qb_name
	, game_result
	, posteam as team
	, defteam as opponent
    , week || ' - ' || opponent as week_opponent
	, count(epa) as plays
	, avg(epa) as avg_epa
from
	plays
group by 1,2,3,4,5
order by 2,1