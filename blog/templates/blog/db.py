from django.http import HttpResponse
import MySQLdb
def get_fname(request, fid):
conn = MySQLdb.connect (host = "localhost",user = "roor",passwd = "",db = "temp")
cursor = conn.cursor ()
cursor.execute ("select * from user")
if cursor.rowcount == 0:
html = "<html><body>There is no Faculty member with id </body></html>"
else:
row = cursor.fetchone()
 html = "<html><body> %s </body></html>"
 % row[0] 
 return HttpResponse(html)