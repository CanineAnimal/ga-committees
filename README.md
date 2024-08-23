# committees
Database and scripts for updating WA committees thread. To run this code, run the Python scripts as follows,

## data_entry.py
This script will save raw data regarding committees into committees.csv, with the data inputted yourself. There are options to add a new committee, and to add a reference to a previously founded committee. This functions entirely offline, and depends only on the Python libraries `csv` and `os`.

## big_generator.py
This script first scrapes a list of repealed resolutions (and repeals themselves) from the API. This list is saved to repeals_cache.txt, meaning that the script does not need to re-scrape repeals or already repealed resolutions! After that, it will use the `committees.csv` database to create two files, `active.txt` and `repeals.txt`. These contain the BBCode for the table of active and repealed committees, respectively, as posted onto the forum thread :D

As it scrapes the API, this script *does* require internet access, as well as the `committees.csv` file. It also uses the libraries `ElementTree`, `requests`, `time`, `csv` and `os`.
