#! /usr/bin/env python3

import cgi, cgitb
import re
import os
import sqlite3
import uuid
import hashlib

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
  <link type="text/css" rel="stylesheet" href="/signup.css" />
  </head>
  <div class="container">
    <form action = "/cgi-bin/signup.py" method = "post">
      <h1>Sign Up</h1>
      <hr>
      
      <label><b>Username</b></label>
      <input type="text" placeholder="Enter Username" name="username" required pattern="^[a-zA-Z0-9._%+-]*$" title="should only contain lowercase, uppercase letters, numbers and symbols '.', '_', '%', '+', '-'">

      <label><b>Password</b></label>
      <input type="password" placeholder="Enter Password" name="password" required pattern="^[a-zA-Z0-9._%+-]*$" title="should only contain lowercase, uppercase letters, numbers and symbols '.', '_', '%', '+', '-'">

      <label><b>Retype Password</b></label>
      <input type="password" placeholder="Retype Password" name="password-retype" required pattern="^[a-zA-Z0-9._%+-]*$" title="should only contain lowercase, uppercase letters, numbers and symbols '.', '_', '%', '+', '-'">

      <div class="clearfix">
        <a href="/cgi-bin/index.py"><button type="button" class="cancelbtn">Cancel</button></a>
        <button type="submit" class="signupbtn">Sign Up</button>
      </div>
    </form>
  </div>
  """)

def html_error(string):
    print("<h3>Error</h3>")
    print("<p>{0}</p>".format(string))
    #print("""<meta http-equiv="refresh" content="2; url=/cgi-bin/signup.py"/>""")

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

form = cgi.FieldStorage() 
method = os.environ['REQUEST_METHOD']

if method == "POST":
  # some content is not filled
  if "username" not in form or "password" not in form or "password-retype" not in form:
    html_header()
    html_error("Please fill in the username, password and password-retype.")
    html_body()
    html_tail()

  else:
    html_header()

    username = form.getvalue("username")
    password = form.getvalue("password")
    password_retype = form.getvalue("password-retype")

    # invalid input
    if not(regex_checking(username) & regex_checking(password) & regex_checking(password_retype)):
      html_error("Invald username, password or password-retype")
      html_body()

    else:
      # password and password-retype are not matched
      if password != password_retype:
        html_error("Password and password retyped are not matched")
        html_body()
      
      else:
        conn = sqlite3.connect('../index.db')
        cursor = conn.cursor()
        # used username
        sql = "SELECT 1 FROM 'user' WHERE username = ?"
        cursor.execute(sql, username)
        data = cursor.fetchall()
        if len(data) != 0:
          html_error("Username has been used")
          html_body()
        
        # can sign up
        else:
          hashed_password = hash_password(password)
          sql = "INSERT INTO 'user' (username,password) VALUES (?,?)"
          cursor.execute(sql, (username, hashed_password))
          conn.commit()
          conn.close()
          print("""<h1>Success</h1>
                  <p>Sign up success</p>
                  <p>Will be redirected to index page in 2 seconds</p>
                  <meta http-equiv="refresh" content="2; url=/cgi-bin/index.py"/>""")
    conn.close()
    html_tail()

# go to sign up page or not using post request
else:
  html_header()
  html_body()
  html_tail()

