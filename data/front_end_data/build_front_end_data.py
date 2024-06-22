import duckdb
import os
import glob

relative_path = '../nflfastr/nflfastR_db.duckdb'
abs_path = os.path.abspath(relative_path)

con = duckdb.connect(database=abs_path, read_only=True)

def run_query(file_path, connection):
    output_dir = "parquet_files"
    os.makedirs(output_dir, exist_ok=True)
    output_file_root = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + '.parquet')

    with open(file_path) as f:
        query = f.read()
    
    data = connection.execute(query).df()
    data.to_parquet(output_file_root)

query_files = glob.glob('queries/*.sql')

[run_query(query, con) for query in query_files]

con.close()