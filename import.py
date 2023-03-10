import sqlite3

def add():
    name = input("Committee name: ")
    cnote = input("Note in committee col.: ")
    res = input("Resolution: ")
    rnote = input("Note in resolution col.: ")
    cur.execute("INSERT INTO committees (name, note, res, res_note) VALUES (?,?,?,?)", (name, cnote, res, rnote))
    con.commit()
    print("Added")
    return

def refer():
    name = input("Committee name: ")
    ref = input("Referring resolution: ")
    cur.execute("SELECT serial FROM committees WHERE name LIKE ?", ("%"+name+"%",))
    s = cur.fetchone()[0]
    cur.execute("INSERT INTO refs VALUES (?,?)", (s, ref))
    con.commit()
    print("Added")
    return

def refound():
    name = input("Committee name: ")
    res = input("Refounding resolution: ")
    cur.execute("SELECT serial FROM committees WHERE name LIKE ?", ("%"+name+"%",))
    s = cur.fetchone()[0]
    cur.execute("INSERT INTO refounds VALUES (?,?)", (s, res))
    cur.execute("UPDATE committees SET refounded = TRUE WHERE serial = ?", (s,))
    con.commit()
    print("Added")
    return

def view():
    tables = "committees", "refs", "resolutions", "refounds"
    for table in tables:
        print()
        print()
        print('Table "{}"\n=================='.format(table))
        cur.execute("SELECT * FROM {}".format(table))
        for row in cur.fetchall():
            print(*row, sep="\t")
    return


con = sqlite3.connect("wacdb")
cur = con.cursor()

ops = """Supported operations:
         [a]dd committee
         add [r]eference to committee
         effect re[f]ounding of committee
         [v]iew a table"""

print(ops)
print("Any other operations should be done on the database itself. (Use transactions!)")
while True:
    op = input("Operation: ").casefold()[0]
    if   op == "a": add()
    elif op == "r": refer()
    elif op == "f": refound()
    elif op == "v": view()
    else: print(ops)
    if input("More? Y/N: ").casefold() == "n": break

con.commit()
con.close()
