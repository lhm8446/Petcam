import MySQLdb, commands, cgi, cgitb

# Create instance of FieldStorage
cgitb.enable()
form = cgi.FieldStorage()

# Get data from fields
data = form.getvalue('userNo')
userNo = str(data)

# DB Connect
db = MySQLdb.connect('150.95.141.66','hotdog','hotdog','dog')
curs = db.cursor()

# get video list
out = commands.getoutput('ls /upload/'+userNo)

list = out.split()

# compare vod list
curs.execute("select * from video v where v.users_no ="+userNo)
temp = curs.fetchall()

rm = []

for i in list:
     if(i.endswith('jpg') or i.endswith('mp3')):
        rm.append(i)
     for j in temp:
        if(i==j[1]):
            rm.append(i)
for r in rm:
        list.remove(r)

#insertDB
if(len(list)!=0):
        for i in list:
                save_name = i
                b = i[7:26]
                c = b.rsplit('-',1)
                regdate = c[0]
                regtime = c[1]
                curs.execute("insert into video (save_name, regdate, regtime, users_no) VALUES('"+save_name+"','"+regdate+"','"+regtime+"')")
else:
        print "no excute"
db.commit()
db.close()