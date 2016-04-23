import urllib, sqlite3, time, os, datetime, smtplib

# Check if DB exist, create it if it doesn't
path = os.getcwd()
DBpath = path + "\CraigsDB"

if os.path.isfile(DBpath):
    nothing = 'nothing'
else:
    conn = sqlite3.connect(DBpath)
    c = conn.cursor()
    c.execute('''create table tbl_Items(address, title, text, email, success, dayOrd)''')
    conn.commit()
    c.close()


while 1:
    # Read Main Page
    while 1:
        try:
            f = urllib.urlopen("http://rapidcity.craigslist.org/zip/")
            freePage = f.read()
            f.close()
            break
        except:
            time.sleep(60) # if page not found, wait before trying again

    # Connect to DB
    conn = sqlite3.connect(DBpath)
    c = conn.cursor()

    # Variable to keep place in html as main webpage is read
    pageSearchPlace = 0

    while 1:
        # get item from main webpage
        itemA = freePage.find('<p class="row">',pageSearchPlace)
        if itemA == -1:
            break
        itemB = freePage.find('<a href="',itemA)+9
        itemC = freePage.find('">', itemB)
        itemAddress = freePage[itemB:itemC]    
        pageSearchPlace = itemC

        #Check DB for Item
        t = (itemAddress,)
        c.execute('SELECT * FROM tbl_Items WHERE address=?', t)
        itemCheck = c.fetchone()
        if itemCheck:
            # if item is in DB do nothing here:
            nothing = "nothing"
        else:
            
            # if item is not found do this:           
            # Read Item Page
            while 1:
                try:
                    f = urllib.urlopen(itemAddress)
                    itemPage = f.read()
                    f.close()
                    break
                except:
                    time.sleep(60)


            titleA = itemPage.find('<h2>')
            titleB = itemPage.find('</h2>')
            title = itemPage[titleA+4:titleB][0:40].strip()
            title = title.replace('(Rapid City)','')
            title = title.replace('(rapid city)','')
            title = title.replace('(Rapid city)', '')
            title = title.replace('(rapid)','')
            title = title.replace('(Rapid)','')            
            title = title.replace('(Sturgis)','')
            title = title.replace('(Box Elder)','')
            title = title.replace('rapid','')
            title = title.replace('Rapid','')
            title = title.replace('City','')
            title = title.replace('city','')
            title = title.replace('Rapid','')
            title = title.replace('(','')
            title = title.replace(')','')
            emailA = itemPage.find('<a href="mailto:')
            # Some ads don't have email so:
            if emailA <> -1:
                emailB = itemPage.find('?',emailA)
                email = itemPage[emailA+16:emailB].strip()
            else:
                email = ''
            textA = itemPage.find('<div id="userbody">')
            textB = itemPage.find('<!-- START CLTAGS -->')
            text = itemPage[textA+19:textB].strip()
            text = text.replace('\n',' ')
            text = text.replace('<br>','')
            text = text.replace('  ',' ')
            messLength = len("Subject: CraigsList \n\n" + title+ '. '+'. '+email)
            text = text[0:172-messLength]
            #print "new item added to DB", itemAddress
            t = (itemAddress, title, text, email, 'no', datetime.date.today().toordinal())
            c.execute('INSERT INTO tbl_Items VALUES (?,?,?,?,?,?)', t)
            conn.commit()
            time.sleep(1) # etiquette: dont hit CraigsList too fast

    # Query DB for unsent items
    t = ('no',)
    c.execute('SELECT * FROM tbl_Items WHERE success=?', t)
    itemCheck = c.fetchall()
    for row in itemCheck:
        try:
            # for each not sent item in DB send:
            uItemAddress = row[0]
            uTitle = row[1]
            uText = row[2]
            uEmail = row[3]
            uSuccess = row[4]
            # send sms
            message = "Subject: CraigsList \n\n" + uTitle+ '. '+uText+'. '+uEmail
            fromaddr = 'johndoe@email.com'
            password = 'password'
            toaddrs = '5558675309@vtext.com'
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo('x')
            server.starttls()
            server.ehlo('x')
            server.login( fromaddr, password)
            server.sendmail(fromaddr, toaddrs,  message)
            
            # then for each item that was just sent, update DB:
            t = (uItemAddress,)
            c.execute("UPDATE tbl_Items SET success='yes' WHERE address=?", t)
            conn.commit()
            time.sleep(10) # sleep before trying to send next sms
        except:
            nothing = 'nothing'
            #print "sms failed, will try again next time"
    #print "Deleting old records and sleeping for 10 minutes"
    t = (datetime.date.today().toordinal()-60,)
    c.execute("DELETE FROM tbl_Items WHERE dayOrd<?", t)
    conn.commit()
    time.sleep(10*60)




c.close()
print "program ended"
