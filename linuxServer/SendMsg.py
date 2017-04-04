import socket
import cgi, cgitb
import os
# Create instance of FieldStorage
cgitb.enable()
form = cgi.FieldStorage()

# Get data from fields
msg = form.getvalue('msg')
ip  = form.getvalue('ip')

UDP_PORT = 8000

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s %s</h2>" % (msg,ip)
print "</body>"
print "</html>"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(msg,(ip, UDP_PORT))
sock.close()