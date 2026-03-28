# Bayesian Analysis of SSBM Matchups

This repo contains code to model matchup spreads in SSBM using Bayesian analysis.

## Source Data

Chart.slp has provided a [database backup](https://chartslp.com/) of Slippi matches. This ~140 GB json file contains plenty of data to analyze, but it must be parsed properly in order to make the data usable in any sort of analysis.

## Script Usage

To parse out the data from the large source file, use the scripts in the following order:

1. `parse_matches.py`: Extracts only the relevant fields from the match data for analysis.
2. `filter_complete_matches.py`: Only consider completed matches, where there is a winner.
3. `filter_by_character.py`: Filter only for matchups between two specified characters.
4. `export_winners_csv.py`: Export relevant match data into a CSV file.
