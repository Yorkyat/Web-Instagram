#! /usr/bin/env python3

import cgi, cgitb
import cookies
import sqlite3
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

def html_error(string):
    print("<h3>Error</h3>")
    print("<p>{0}</p>".format(string))
    print("<p>Will be redirected to index page in 2 seconds</p>")
    print("""<meta http-equiv="refresh" content="2; url=/cgi-bin/index.py"/>""")

conn = sqlite3.connect('../index.db')
cursor = conn.cursor()
sql = "SELECT * FROM sqlite_master WHERE name ='user' and type='table'"
cursor.execute(sql)
result = cursor.fetchone()
conn.close()
# first user
if result == None:
    html_header()
    print("""
    <meta http-equiv="refresh" content="0; url=/cgi-bin/init_changepw.py"/>
    """)
    html_tail()

else:
    cookie = cookies.create_cookies()
    session_id = cookies.retrieve_cookies(cookie, 'session')

    if session_id == False:
        html_header()
        html_error("Please login first")
        html_tail()
    else:
        username = cookies.retrieve_username(session_id)
        if username != "Admin":
            html_header()
            html_error("Only admin can initialize!")
            html_tail()
        else:
            conn = sqlite3.connect('../index.db')
            cursor = conn.cursor()

            sql = "DROP TABLE IF EXISTS `image`"
            cursor.execute(sql)

            sql = "CREATE TABLE 'image'(`pid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,`image` TEXT NOT NULL UNIQUE,`mode` TEXT NOT NULL,`username` TEXT,`timestamp` TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
            cursor.execute(sql)

            dirs = os.listdir("./tmp/")
            for file in dirs:
                if file != ".gitignore":
                    os.remove("./tmp/" + file)

            dirs = os.listdir("./img/")
            for file in dirs:
                if file != ".gitignore":
                    os.remove("./img/" + file)
            
            html_header()
            print("""
            <div class="container text-center my-3">
                <div>
                    <h1>Success</h1>
                    <p>Initialization completes</p>
                </div>
            </div>
            <div class="container text-center">
                <a href="/cgi-bin/index.py"><button type="button" class="btn btn-primary mx-3 text-center">Back to Index Page</button></a>
            </div>
            """)
            html_tail()
