#! /usr/bin/env python3

import cgi
import cgitb;cgitb.enable()
import re
import os
import sqlite3
import cookies

def html_header():
  print("""Content-Type: text/html\r\n
  <!DOCTYPE html>
  <html>""")

def html_tail():
  print("""
  </html>
  """)

def html_error(string):
    print("<h3>Error</h3>")
    print("<p>{0}</p>".format(string))
    print("<p>Will be redirected to index page in 2 seconds</p>")
    print("""<meta http-equiv="refresh" content="2; url=/cgi-bin/index.py"/>""")

def regex_checking(string):
  p = re.compile("^[a-zA-Z0-9-_ ]*$")
  result = p.match(string)
  if result == None:
    return False
  else:
    return True

cookie = cookies.create_cookies()
session_id = cookies.retrieve_cookies(cookie)

if session_id == False:
  html_header()
  html_error("Please Login")
  html_tail()

form = cgi.FieldStorage()

# Get filename here.
fileitem = form['filename']

# Test if the file was uploaded
if fileitem.filename:
  # strip leading path from file name to avoid 
  # directory traversal attacks
  fn = os.path.basename(fileitem.filename)
  open('./tmp/' + fn, 'wb').write(fileitem.file.read())
  
  html_header()
  print("""
  <meta http-equiv="refresh" content="0; url=/cgi-bin/index.py"/>
  """)
  html_tail()
else:
  html_header()
  html_error("No file was uploaded")
  html_tail()
