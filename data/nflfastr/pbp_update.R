# Load necessary libraries
library(nflfastR)
library(DBI)
library(duckdb)


# Connect to DuckDB database
db_path <- "/Users/chris.fenton/projects/nfl_app/nfl_evidence/sources/nflfastR_db.duckdb"
con <- dbConnect(duckdb::duckdb(), db_path)

most_recent_pbp <- nflfastR::load_pbp()
max_season <- max(most_recent_pbp$season)


#delete most recent season
dbExecute(con, paste0("DELETE FROM pbp_data WHERE season = ",max_season))



# Function to download and load full play-by-play data
load_most_recent_pbp_data <- function(con) {
  # Download full play-by-play data
  pbp_data <- nflfastR::load_pbp(seasons=(max_season))
  
  # Write data to DuckDB
  dbWriteTable(con, "pbp_data", pbp_data, append = TRUE)
  
  message(paste0("pbp records updated for ",max_season," season"))
}

# Load full play-by-play data initially
load_most_recent_pbp_data(con)


# Close the connection
dbDisconnect(con)
