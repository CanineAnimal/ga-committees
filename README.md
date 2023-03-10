# committees
Database and scripts for updating WA committees thread

## The database
The database (named `wacdb` for WA committee database) uses SQLite. It contains the following tables:
### Table `committees`
The main table that contains each committee.

|Column|Type|Remark|
|---|---|---|
|serial|INTEGER|Serial number, unique to each committee (primary key). The number has no meaning in itself, it is just unique for each committee so that it can be used to cross-reference between committees.|
|name|VARCHAR(500)|Name of committee|
|note|VARCHAR(500)|Note to be included in the committee column of the generated output table|
|res|INT|Resolution number in which it was founded originally|
|res_note|VARCHAR(500)|Note to be included in the resolution column of the generated output table|
|refounded|BOOLEAN|Whether the committee was refounded|

### Table `refounds`
Contains every instance of a repealed committee being refounded.

|Column|Type|Remark|
|---|---|---|
|serial|INT|The same serial number as in `committees`|
|res|INT|Resolution number in which it was refounded|

### Table `refs`
Contains references to committees in other resolutions. If a committee is referenced in multiple resolutions, each reference has a row.

|Column|Type|Remark|
|---|---|---|
|serial|INT|As above|
|res|INT|Resolution number in which it was referred to|

### Table `resolutions`
Contains each GA resolution, its name and the URL of its post in the GA forum list of resolutions.

|Column|Type|Remark|
|---|---|---|
|res|INT|Resolution number|
|url|VARCHAR(500)|Link to the gameside resolution page (e.g., https://www.nationstates.net/page=WA_past_resolution/id=532/council=1)|
|resname|VARCHAR(500)|Resolution name|
|repealed|BOOLEAN|Whether the resolution has been repealed|


## The scripts
There are three scripts included:
* `import.py`
* `export.py`
* `posts.py`

### `import.py`
This script is used for making entries in the database. It runs interactively and prints instructions on the screen. It supports the following operations:
* adding a committee
* adding a reference to a committee
* refounding a repealed committee
* viewing the database's tables.

These are the usual operations necessary when updating the list for new resolutions. Anything else can be done directly on the database using SQL commands. 

### `export.py`
This script generates the BBcode tables from the database automatically. It needs no user input. It outputs three text files:
* `active.txt` contains the table of committees founded/refounded in active resolutions
* `repealed.txt` contains committees founded in repealed resolutions
* `footer.txt` contains the footnotes.

### `posts.py`
This script uses the NS API to build the "resolutions" table. It checks the existing entries in the table and queries the API for the resolutions not already included. It automatically marks resolutions as repealed if the repealing resolution is found. (Note: the name of the script is historical, since in its initial version it scraped the List of Passed Resolutions on the NS forum.)


## Workflow for updating the committee list
1. Run `posts.py`.
2. Start `import.py`.
3. Go through the resolutions passed since last update, looking for any new committees/refoundings/references to be added. Add each one following the on-screen instructions of `import.py`.
4. Run `export.py`.
5. Replace the table in the "active resolutions" post with the content of `active.txt`, and that in the "repealed resolutions" post with `repealed.txt`.
6. Add the contents of `footer.txt` in an appropriate place.
