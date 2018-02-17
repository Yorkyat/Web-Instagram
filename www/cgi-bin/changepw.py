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
    <form action = "/cgi-bin/changepw.py" method = "post">
      <h1>Change Password</h1>
      <hr>

      <label><b>Current Password</b></label>
      <input type="password" placeholder="Enter Current Password" name="password-old" required pattern="^[a-zA-Z0-9._%+-]*$" title="should only contain lowercase, uppercase letters, numbers and symbols '.', '_', '%', '+', '-'">

      <label><b>New Password</b></label>
      <input type="password" placeholder="Enter New Password" name="password-new" required pattern="^[a-zA-Z0-9._%+-]*$" title="should only contain lowercase, uppercase letters, numbers and symbols '.', '_', '%', '+', '-'">

      <label><b>Retype New Password</b></label>
      <input type="password" placeholder="Retype New Password" name="password-retype" required pattern="^[a-zA-Z0-9._%+-]*$" title="should only contain lowercase, uppercase letters, numbers and symbols '.', '_', '%', '+', '-'">

      <div class="clearfix">
        <a href="/cgi-bin/index.py"><button type="button" class="cancelbtn">Cancel</button></a>
        <button type="submit" class="updatebtn">Update</button>
      </div>
    </form>
  </div>
  """)

def html_error(string):
    print("<h3>Error</h3>")
    print("<p>{0}</p>".format(string))
    print("""<meta http-equiv="refresh" content="2; url=/cgi-bin/index.py"/>""")

def html_extend_cookies(session_id, cookie):
  if session_id:
    cookies.cookies_extend(cookie, 'session')
    cookies.cookies_head(cookie)

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

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

# check table exist
def check_user_table_exist(c):
    sql = "CREATE TABLE IF NOT EXISTS `user` (`uid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,`username` TEXT NOT NULL UNIQUE,`password` TEXT NOT NULL)"
    c.execute(sql)
  
form = cgi.FieldStorage() 
method = os.environ['REQUEST_METHOD']

cookie = cookies.create_cookies()
session_id = cookies.retrieve_session_cookies(cookie, 'session')
html_extend_cookies(session_id, cookie)

if session_id == False:
  html_header()
  print("""<meta http-equiv="refresh" content="0; url=/cgi-bin/index.py"/>""")
  html_tail()
else:
  if method == "POST":
    # some content is not filled
    if "password-old" not in form or "password-new" not in form or "password-retype" not in form:
      html_header()
      html_error("Please fill in the old password, new password and retyped password.")
      html_body()
      html_tail()
    
    else:  
      username = cookies.retrieve_username(session_id)
      password_old = form.getvalue("password-old")
      password_new = form.getvalue("password-new")
      password_retype = form.getvalue("password-retype")

      # invalid input
      if not(regex_checking(password_old) & regex_checking(password_new) & regex_checking(password_retype)):
        html_header()
        html_error("Invalid old password, new password or retyped password")

      else:
        # password_new and password_retype are not matched
        if password_new != password_retype:
          html_header()
          html_error("New password and password retyped are not matched")

        else:
          conn = sqlite3.connect('../index.db')
          cursor = conn.cursor()
          check_user_table_exist(cursor)

          sql = "SELECT `password` FROM `user` WHERE `username` = ?"
          cursor.execute(sql, (username,))
          data = cursor.fetchone()
          db_password = data[0]

          # same as old password
          if check_password(db_password, password_new):
            html_header()
            html_error("Change password fails")
            html_tail()

          # hash the password and update
          else:
            hashed_password = hash_password(password_new)
            sql = "UPDATE `user` SET `password` = ? WHERE `username` = ?"
            cursor.execute(sql, (hashed_password, username,))
            conn.commit()
            conn.close()
            html_header()
            print("""<h1>Success</h1>
                    <p>Change password success</p>
                    <p>Will be redirected to index page in 2 seconds</p>
                    <meta http-equiv="refresh" content="2; url=/cgi-bin/index.py"/>""")
    html_tail()

  # go to change password page or not using post request
  else:
    html_header()
    html_body()
    html_tail()
