import duckdb
import os

relative_path = '../nflfastr/nflfastR_db.duckdb'
abs_path = os.path.abspath(relative_path)

con = duckdb.connect(database = abs_path
                     , read_only = True)

with open('queries/first_down_query.sql') as f:
    first_down_query = f.read()

df = con.execute(first_down_query).df()


df.to_parquet('first_down.parquet')

with open('queries/qb_epa.sql') as f:
    qb_epa_query = f.read()

df = con.execute(qb_epa_query).df()
df.to_parquet('qb_epa.parquet')

con.close()