import datetime, sqlite3

conn = sqlite3.connect('Z:\Data\Scripts\CraigsListFree\CraigsDB')
c = conn.cursor()

t = ('http://rapidcity.craigslist.org/zip/2872652615.html',)
c.execute("DELETE FROM tbl_Items WHERE address=?", t)
conn.commit()

