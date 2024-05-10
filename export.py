import sqlite3

def findres(res): # returns name and URL
    x = cur.execute("SELECT resname, url FROM resolutions WHERE res = ?", (res,)).fetchone()
    return x[0], x[1]

def findrepealed(res): # returns whether the resolution is repealed
    x = cur.execute("SELECT repealed FROM resolutions WHERE res = ?", (res,)).fetchone()
    return x[0]

header = "[tr][td][sup][/sup][b]Committee[/b][/td][td][sup][/sup][b]Creating resolution[/b][/td][td][sup][/sup][b]Referring resolutions[/b][/td][/tr]"
active = "[table]" + header
repealed = "[table]" + header
footer = "[b]Footnotes:[/b]\n[list=1]"
notecount = 1
rowfmt = "[tr][td]{cname}[sup]{cnote}[/sup][/td][td][url={url}]GA {res}: {resname}[/url]{refound}[sup]{resnote}[/sup][/td][td]{reflist}[/td][/tr]"
reffmt = "[url={refurl}]{refres}[/url], "
refoundfmt = ", refounded in [url={rfurl}]GA {rfres}: {rfresname}[/url]"

con = sqlite3.connect("wacdb")
cur = con.cursor()

cur.execute("SELECT committees.name, note, committees.res, res_note, resolutions.repealed, refounded, serial FROM committees, resolutions WHERE resolutions.res = committees.res ORDER BY committees.res")
rows = cur.fetchall()

for row in rows:
    cname = row[0]
    cnotetext = row[1]
    res = row[2]
    resnotetext = row[3]
    isrepealed = row[4]
    isrefounded = row[5]
    serial = row[6]
    resname, url = findres(res)
    reflist = ""
    refoundlist = ""
    cnote = ""
    resnote = ""

    # references
    cur.execute("SELECT res FROM refs WHERE serial = ? ORDER BY res", (serial,))
    refrows = cur.fetchall()
    for ref in refrows:
        refurl = findres(ref[0])[1]
        refentry = reffmt.format(refurl=refurl, refres=ref[0])
        reflist += refentry

    reflist = reflist.rstrip(', ')

    if isrefounded:
        cur.execute("SELECT res FROM refounds WHERE serial = ? ORDER BY res", (serial,))
        refoundrows = cur.fetchall()
        if len(refoundrows) > 1:
            print(f"More than one refound for committee {serial} ({refoundrows})!")
        for refounding in refoundrows:
            refname, refurl = findres(refounding[0])
            refentry = refoundfmt.format(rfurl=refurl, rfres=refounding[0], rfresname=refname)
            refoundlist += refentry

        lastrefound = refoundrows[-1][0]
        isrepealed = findrepealed(lastrefound) # When a committee has been refounded, check the status of the last refound, not original res

    if cnotetext:
        cnote = notecount
        footer += f"[*]{cnotetext}\n"
        notecount += 1

    if resnotetext:
        resnote = notecount
        footer += f"[*]{resnotetext}\n"
        notecount += 1

    entry = rowfmt.format(cname=cname, cnote=cnote, url=url, res=res, resname=resname, refound=refoundlist, resnote=resnote, reflist=reflist)
    if isrepealed:
        repealed += entry
    else:
        active += entry

active += "[/table]"
repealed += "[/table]"
footer += "[/list]"

blockers = '[table][tr][td][b]Resolution[/b][/td][td][b]Scope[/b][/td][td][b]Exceptions[/b][/td][td][b]Blocker text[/b][/td][/tr]';
g = open('blockers.csv', 'r')
blockers2 = g.read().split('\n')
g.close()
for blocker in blockers2:
    blockers += '[tr][td][url=https://www.nationstates.net/page=WA_past_resolution/id=' + blocker.split(',')[0] + '/council=1]GA #' + blocker.split(',')[0] + '[/url], §' + blocker.split(',')[1] + '[/td][td]' + blocker.split(',')[2] + '[/td][td]' + blocker.split(',')[3] + '[/td][td]' + blocker.split(',')[4] + '[/td][/tr]';
blockers += '[/table]'

with open("active.txt", "w") as f: f.write(active)
with open("repealed.txt", "w") as f: f.write(repealed)
with open("footer.txt", "w") as f: f.write(footer)
with open("blockers.txt", "w") as f: f.write(blockers)
