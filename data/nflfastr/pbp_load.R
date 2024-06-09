# Load necessary libraries
library(nflfastR)
library(DBI)
library(duckdb)
library(here)

here::i_am("data/nflfastr/pbp_update.R")
db_path <- here("data", "nflfastr", "nflfastR_db.duckdb")

# Connect to DuckDB database
con <- dbConnect(duckdb::duckdb(), db_path)

# Function to download and load full play-by-play data
load_full_pbp_data <- function(con) {
  # Download full play-by-play data
  pbp_data <- nflfastR::load_pbp(seasons=TRUE)
  
  # Write data to DuckDB
  dbWriteTable(con, "pbp_data", pbp_data, overwrite = TRUE)
  message("Full play-by-play data loaded successfully.")
}


# Load full play-by-play data initially
load_full_pbp_data(con)

# Update play-by-play data for the most recent season (change the year accordingly)
#update_recent_season_pbp_data(con, 2024)

# Close the connection
dbDisconnect(con)
