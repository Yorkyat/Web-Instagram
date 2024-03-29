#! /usr/bin/env python3

import cookies
import sqlite3

def html_header():
  print("""Content-Type: text/html\r\n
  <!DOCTYPE html>
  <html>""")

def html_tail():
  print("""
  </html>
  """)

cookie = cookies.create_cookies()
session_id = cookies.retrieve_cookies(cookie, 'session')

if session_id == False:
  html_header()
  print("""<meta http-equiv="refresh" content="0; url=/cgi-bin/index.py"/>""")
  html_tail()
else:
    cookies.del_cookies(cookie, 'session')
    if cookies.retrieve_cookies(cookie, 'upload-mode'):
      cookies.del_cookies(cookie, 'upload-mode')
    if cookies.retrieve_cookies(cookie, 'image'):
      cookies.del_cookies(cookie, 'image')
    conn = sqlite3.connect('../index.db')
    cursor = conn.cursor()
    cookies.del_session_id(session_id, cursor, conn)
    conn.close()

    cookies.cookies_head(cookie)
    html_header()
    print("""<h1>Success</h1>
            <p>Logout success</p>
            <p>Will be redirected to index page in 2 seconds</p>
            <meta http-equiv="refresh" content="2; url=/cgi-bin/index.py"/>""")
    html_tail()