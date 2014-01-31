import MySQLdb

dbname = 'threegoodthings'
dbuser = 'threegoodthings'
dbpass = 'pHad4f3s'
dbhost = 'mysql.logicalrealism.org'

d = MySQLdb.connect(dbhost,dbuser,dbpass,dbname)
c = d.cursor(MySQLdb.cursors.DictCursor)

fbuid = '2220453'
c.execute("SELECT user_id FROM member_userprofile WHERE facebook_id="+fbuid+"")
uid = c.fetchone()['user_id']

c.execute("SELECT * FROM gt WHERE uid="+fbuid+"")
rows = c.fetchall()

for row in rows:
    gt = {}
    gt['gt'] = row['text']
    gt['created'] = row['created']
    gt['public'] = row['public']
    gt['wall'] = row['wall']
    gt['uid'] = uid
    
    c.execute("SELECT `text` FROM reasons WHERE gtid="+str(row['gtid']))
    if int(c.rowcount) != 0:
        gt['reason'] = c.fetchone()['text']
        q = """INSERT INTO tgt_goodthing (goodThing,reason,posted,user_id,public,wall) VALUES(%(gt)s,%(reason)s,%(created)s,%(uid)s,%(public)s,%(wall)s)"""
    else:
        pass
        q = """INSERT INTO tgt_goodthing (goodThing,posted,user_id,public,wall) VALUES(%(gt)s,%(created)s,%(uid)s,%(public)s,%(wall)s)"""
    c.execute(q,gt)

d.close()


