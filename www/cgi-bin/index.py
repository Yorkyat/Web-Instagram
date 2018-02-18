#! /usr/bin/env python3

import cgi, cgitb
import sqlite3
import cookies
import math
import os

def html_header():
  print("""Content-Type: text/html\r\n
  <!DOCTYPE html>
  <html>
  <head>
  <link type="text/css" rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  </head>
  <body>""")

def html_tail():
  print("""
  </body>
  </html>
  """)

def html_username(username):
    print("""
    <div class="container text-right my-2">
    <h5>Username: {0}</h5>
    </div>
    """.format(username))

def html_account(session_id):
  if session_id:
    print("""
    <div class="container text-right">
      <a class="btn btn-primary mr-1" href="/cgi-bin/changepw.py">Change Password</a>
      <a class="btn btn-primary ml-1" href="/cgi-bin/logout.py">Logout</a>
    </div>
    <hr>
    """)
  else:
    print("""
    <div class="container text-right my-3">
      <a class="btn btn-primary mr-1" href="/cgi-bin/login.py">Login</a>
      <a class="btn btn-primary ml-1" href="/cgi-bin/signup.py">Sign Up</a>
    </div>
    <hr>
    """)

def html_extend_cookies(session_id, cookie):
  if session_id:
    cookies.cookies_extend(cookie, 'session')
    cookies.cookies_head(cookie)

def check_img_table_exist(c):
    sql = "CREATE TABLE IF NOT EXISTS 'image'(`pid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,`image` TEXT NOT NULL UNIQUE,`mode` TEXT NOT NULL,`username` TEXT,`timestamp` TEXT NOT NULL)"
    c.execute(sql)

def html_index(session_id):
  form = cgi.FieldStorage()
  page_no = 0
  page_total = 1
  if "page_no" not in form:
    page_no = 1
  else:
    page_no = int(form.getvalue("page_no"))

  conn = sqlite3.connect('../index.db')
  cursor = conn.cursor()
  check_img_table_exist(cursor)

  sql = ""
  if session_id:
    username = cookies.retrieve_username(session_id)
    sql = "SELECT `image` FROM `image` WHERE `mode` = 'public' OR (`mode` = 'private' AND `username` = ?) ORDER BY `timestamp` DESC"
    cursor.execute(sql, (username,))
  else:
    sql = "SELECT `image` FROM `image` WHERE `mode` = 'public' ORDER BY `timestamp` DESC"
    cursor.execute(sql)
  
  images = cursor.fetchall()
  conn.close()

  no_of_photo = len(images)

  # multiple of 8
  if no_of_photo != 0:
    page_total = math.ceil(no_of_photo / 8)

  if page_no > page_total:
    print("""<meta http-equiv="refresh" content="0; url=/cgi-bin/index.py"/>""")
  else:
    print("""
    <div class="container text-center">
      <div class="row justify-content-center text-center">
    """)

    index = 0
    for i in images:
      if ((index >= (8 * (page_no - 1)) and (index < (8 * page_no)) and (index <= (no_of_photo - 1)))):
        print("""
        <div class="card text-center justify-content-center align-self-center" style="height: 202px ; width: 202px;">
          <a href={0}>
            <img style="max-height: 200px; max-width: 200px; width: auto; height: auto" src={0}>
          </a>
        </div>
        """.format("/img/"+images[index][0]))
      index += 1

    print("""
      </div>
    </div>
    """)

    # pagination
    print("""
    <form action = "/cgi-bin/index.py" method = "get">
      <div class="container text-center my-3">
    """)

    if page_no == 1:
      print("""<button type="button" class="btn btn-primary mx-3 disabled">Previous Page</button>""")
    else:
      print("""<a href="/cgi-bin/index.py?page_no={0}"><button type="button" class="btn btn-primary mx-3">Previous Page</button></a>""".format(page_no - 1))

    print("""<input style="width: 30px" type="text" value="{0}" name="page_no" required pattern="^[0-9]*$"> / {1}""".format(page_no, page_total))
    
    if page_no == page_total:
      print("""<button type="button" class="btn btn-primary mx-3 disabled">Next Page</button>""")
    else:
      print("""<a href="/cgi-bin/index.py?page_no={0}"><button type="button" class="btn btn-primary mx-3">Next Page</button></a>""".format(page_no + 1))

    print("""
      </div>
    </form>
    """)

def html_upload(session_id):
  if session_id:
    print("""
    <hr>
    <form enctype = "multipart/form-data" action = "upload.py" method = "post">
      <div class="container text-center my-3">
        <span class="mx-3">Upload Photo</span>
        <input class="btn btn-primary mx-1" type = "file" name = "filename" accept="image/*" />
        <input class="btn btn-primary mx-1" type = "submit" value = "Upload" />
        <input class="ml-3" type = "radio" name = "upload-mode" value = "public" checked="checked" /> Public
        <input type = "radio" name = "upload-mode" value = "private" /> Private
      </div>
    </form>
    """)

if not os.path.exists('./tmp/'):
  os.makedirs('./tmp/')

cookie = cookies.create_cookies()
session_id = cookies.retrieve_cookies(cookie, 'session')

html_extend_cookies(session_id, cookie)
html_header()

if session_id:
  username = cookies.retrieve_username(session_id)
  html_username(username)

html_account(session_id)
html_index(session_id)
html_upload(session_id)
html_tail()