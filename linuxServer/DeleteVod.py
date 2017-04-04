import cgi, cgitb
import os

# Create instance of FieldStorage
cgitb.enable()
form = cgi.FieldStorage()

# Get data from fields
userNo = form.getvalue('userNo')
name  = form.getvalue('name')

path = str("sudo rm -f /upload/"+userNo+"/"+name)

os.system(path)
