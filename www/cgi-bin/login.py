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
    <link type="text/css" rel="stylesheet" href="/login.css" />
    </head>
    <div class="container">
    <form action = "/cgi-bin/login.py" method = "post">
        <h1>Login</h1>
        <hr>

        <label><b>Username</b></label>
        <input type="text" placeholder="Enter Username" name="username" required pattern="^[a-zA-Z0-9._%+-]*$" title="should only contain lowercase, uppercase letters, numbers and symbols '.', '_', '%', '+', '-'">

        <label><b>Password</b></label>
        <input type="password" placeholder="Enter Password" name="password" required pattern="^[a-zA-Z0-9._%+-]*$" title="should only contain lowercase, uppercase letters, numbers and symbols '.', '_', '%', '+', '-'">

        <div class="clearfix">
        <a href="/cgi-bin/index.py"><button type="button" class="cancelbtn">Cancel</button></a>
        <button type="submit" class="loginbtn">Login</button>
        </div>
    </form>
    </div>
    </body>
    """)

def html_error(string):
    print("<h3>Error</h3>")
    print("<p>{0}</p>".format(string))
    print("<p>Will be redirected to index page in 2 seconds</p>")
    print("""<meta http-equiv="refresh" content="2; url=/cgi-bin/index.py"/>""")

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

def check_user_table_exist(c):
    sql = "CREATE TABLE IF NOT EXISTS 'user'('uid' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 'username' TEXT NOT NULL UNIQUE, 'password' TEXT NOT NULL)"
    c.execute(sql)

form = cgi.FieldStorage() 
method = os.environ['REQUEST_METHOD']

if method == "POST":
  # some content is not filled
  if "username" not in form or "password" not in form:
    html_header()
    html_error("Please fill in the username, password.")
    html_tail()

  else:
    username = form.getvalue("username")
    password = form.getvalue("password")

    # invalid input
    if not(regex_checking(username) & regex_checking(password)):
      html_header()
      html_error("Invalid username, password")

    else:
        conn = sqlite3.connect('../index.db')
        cursor = conn.cursor()
        check_user_table_exist(cursor)

        # check username exists
        sql = "SELECT password FROM 'user' WHERE username = ?"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()

        # username exists
        if data != None:
            # check password correct
            db_password = data[0]
            if check_password(db_password, password):
                # set session id
                session_id = cookies.set_session_id(username, cursor, conn)
                # set cookies
                cookie = cookies.create_cookies()
                cookies.set_cookies(cookie, session_id)

                cookies.cookies_head(cookie)
                html_header()
                print("""<h1>Success</h1>
                        <p>Login success</p>
                        <p>Will be redirected to index page in 2 seconds</p>
                        <meta http-equiv="refresh" content="2; url=/cgi-bin/index.py"/>""")


            # incorrect password
            else:
                html_header()
                html_error("Incorrect username or password")


        # username not exist
        else:
            html_header()
            html_error("Incorrect username or password")

    conn.close()
    html_tail()

else:
  html_header()
  html_body()
  html_tail()
