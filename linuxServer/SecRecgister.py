import cgi, cgitb
import os
# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
nickname = form.getvalue('nickname')
password  = form.getvalue('password')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s %s</h2>" % (nickname, password)
print "</body>"
print "</html>"

APPEND = "\n"+nickname+" "+password
FILE = "/usr/local/WowzaStreamingEngine/conf/publish.password"
os.system("sudo echo \"$(cat "+FILE+")"+APPEND+" \" >"+FILE)