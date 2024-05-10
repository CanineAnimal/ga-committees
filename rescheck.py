import requests
import sqlite3
from bs4 import BeautifulSoup
import time

maxres = int(input("Enter the number of the latest GA resolution: "))

con = sqlite3.connect("wacdb")
cur = con.cursor()

# Find all the resolutions that have been stored so far
response = cur.execute("SELECT res FROM resolutions")
resol = response.fetchall()
resolutions = [i for t in resol for i in t]
print("Already stored: ", resolutions)
fetchres = []

# Make a list of those that haven't been stored
for i in range(1, maxres+1):
    if i not in resolutions: fetchres.append(i)


# NS API headers
url = "https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=resolution"
headers = {"User-Agent": "Merni's GA committees script (experimental)"}

# Get each resolution
for res in fetchres:
    time.sleep(1)
    r = requests.get(url, headers=headers, params={'id': str(res)})
    data = r.text
    soup = BeautifulSoup(data, "xml")

    resnum = soup.find("COUNCILID").get_text()
    if resnum != str(res):
        print(f"Error! Asked {r.url} for {repr(res)}, got {repr(resnum)}")
        continue

    resurl = f"https://www.nationstates.net/page=WA_past_resolution/id={resnum}/council=1"
    resname = soup.find("NAME").get_text()

    if not soup.find("REPEALED"):
        # This is not repealed
        repealed = False
    else:
        repealed = True
        f = open('blockers.csv', 'r')
        blockers = f.read().split('\n');
        new_csv = '';
        f.close();
        for blocker in blockers:
            if blocker.split(',')[0] != resnum:
                new_csv += blocker.split(',')[0] + ',' + resname + '\n'
        
        f = open('blockers.csv', 'w')
        f.write(new_csv)
        f.close()

    cur.execute("INSERT INTO resolutions (res, resname, url, repealed) VALUES (?, ?, ?, ?)", (resnum, resname, resurl, repealed))
    con.commit()

    print("Done", res)

con.commit()
con.close()
