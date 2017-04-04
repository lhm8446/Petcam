import cgi, cgitb
import os
# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
userno = form.getvalue('userno')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s</h2>" % (userno)
print "</body>"
print "</html>"

os.system("mkdir /upload/"+userno)