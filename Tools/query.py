import sqlite3

conn = sqlite3.connect('Z:\Data\Scripts\CraigsListFree\CraigsDB')

c = conn.cursor()

c.execute('select * from tbl_Items')

for row in c:
    print row

c.close()
