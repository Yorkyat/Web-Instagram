#! /usr/bin/env python3

import cgi, cgitb
import re
import os
import sqlite3
import uuid
import hashlib
import cookies

def html_header():
  print("""Content-Type: text/html\r\n
  <!DOCTYPE html>
  <html>""")

def html_tail():
  print("""
  </html>
  """)

def html_body():
  print("""
  <head>
  <link type="text/css" rel="stylesheet" href="/changepw.css" />
  </head>
  <div class="container">
    <form action = "/cgi-bin/init_changepw.py" method = "post">
      <h1>Create Password</h1>
      <h3>Username: Admin</h3>
      <hr>

      <label><b>Password</b></label>
      <input type="password" placeholder="Enter Password" name="password" required pattern="^[a-zA-Z0-9._%+-]*$" title="should only contain lowercase, uppercase letters, numbers and symbols '.', '_', '%', '+', '-'">

      <label><b>Retype Password</b></label>
      <input type="password" placeholder="Retype Password" name="password-retype" required pattern="^[a-zA-Z0-9._%+-]*$" title="should only contain lowercase, uppercase letters, numbers and symbols '.', '_', '%', '+', '-'">

      <div class="clearfix">
        <a href="/init.html"><button type="button" class="cancelbtn">Cancel</button></a>
        <button type="submit" class="updatebtn">Save</button>
      </div>
    </form>
  </div>
  """)

def html_error(string):
    print("<h3>Error</h3>")
    print("<p>{0}</p>".format(string))
    print("""<meta http-equiv="refresh" content="2; url=/cgi-bin/init_changepw.py"/>""")


def regex_checking(string):
  p = re.compile("^[a-zA-Z0-9._%+-]*$")
  result = p.match(string)
  if result == None:
    return False
  else:
    return True

def hash_password(password):
  salt = uuid.uuid4().hex
  return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

# check table exist
def create_user_table(c):
    sql = "CREATE TABLE `user` (`uid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,`username` TEXT NOT NULL UNIQUE,`password` TEXT NOT NULL)"
    c.execute(sql)
  
form = cgi.FieldStorage() 
method = os.environ['REQUEST_METHOD']

conn = sqlite3.connect('../index.db')
cursor = conn.cursor()
sql = "SELECT * FROM sqlite_master WHERE name ='user' and type='table'"
cursor.execute(sql)
result = cursor.fetchone()
conn.close()

if result != None:
  html_header()
  print("""<meta http-equiv="refresh" content="0; url=/cgi-bin/index.py"/>""")
  html_tail()
else:
  if method == "POST":
    # some content is not filled
    if "password" not in form or "password-retype" not in form:
      html_header()
      html_error("Please fill in the password and retyped password.")
      html_body()
      html_tail()
    
    else:  
      username = "Admin"
      password = form.getvalue("password")
      password_retype = form.getvalue("password-retype")

      # invalid input
      if not(regex_checking(password) & regex_checking(password_retype)):
        html_header()
        html_error("Invalid password or retyped password")

      else:
        # password_new and password_retype are not matched
        if password != password_retype:
          html_header()
          html_error("Password and password retyped are not matched")

        else:
          conn = sqlite3.connect('../index.db')
          cursor = conn.cursor()
          create_user_table(cursor)

          # hash the password and save
          hashed_password = hash_password(password)
          sql = "INSERT INTO `user` (`username`,`password`) VALUES (?,?)"
          cursor.execute(sql, (username, hashed_password,))
          conn.commit()

          session_id = cookies.set_session_id(username, cursor, conn)
          cookie = cookies.create_cookies()
          cookies.set_cookies(cookie, 'session', session_id)

          cookies.cookies_head(cookie)
          html_header()
          print("""<h1>Success</h1>
                  <p>Login Admin account</p>
                  <p>Will start to initialize in 2 seconds</p>
                  <meta http-equiv="refresh" content="2; url=/cgi-bin/init.py"/>""")
    conn.close()
    html_tail()

  # go to change password page or not using post request
  else:
    html_header()
    html_body()
    html_tail()
