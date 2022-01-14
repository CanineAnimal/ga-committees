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
|repealed|BOOLEAN|Whether the committee is to be included in the "Repealed committees" section|
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
|url|VARCHAR(500)|URL of its post in the GA forum list of resolutions|
|resname|VARCHAR(500)|Resolution name|


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
* repealing a committee
* viewing the database's tables.

These are the usual operations necessary when updating the list for new resolutions. Anything else can be done directly on the database using SQL commands. 

### `export.py`
This script generates the BBcode tables from the database automatically. It needs no user input. It outputs three text files:
* `active.txt` contains the table of committees founded/refounded in active resolutions
* `repealed.txt` contains committees founded in repealed resolutions
* `footer.txt` contains the footnotes.

### `posts.py`
This script, a substantially modified form of https://github.com/ifly6/RexisQuexis/blob/master/python_scripts/make_postlist.py , generates the `resolutions` table in the database by scraping the NS forums.


## Workflow for updating the committee list
1. Run `posts.py`.
2. Start `import.py`.
3. Go through the Passed Resolutions thread, looking for any new committees/refoundings/repeals/references to be added. Add each one following the on-screen instructions of `import.py`.
4. Run `export.py`.
5. Replace the table in the "active resolutions" post with the content of `active.txt`, and that in the "repealed resolutions" post with `repealed.txt`.
6. Add the contents of `footer.txt` in an appropriate place.
