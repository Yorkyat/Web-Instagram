#! /usr/bin/env python3

import cgi, cgitb
import re
import os
import sqlite3
import cookies
import subprocess
import uuid

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

def html_extend_cookies(session_id, cookie):
  if session_id:
    cookies.cookies_extend(cookie, 'session')
    cookies.cookies_head(cookie)

def regex_checking(string):
  p = re.compile("^[a-zA-Z0-9-_ ]*$")
  result = p.match(string)
  if result == None:
    return False
  else:
    return True
  
def check_file_extension_name(string):
  return string.endswith(('.jpg', '.gif', '.png'))

def retrieve_file_type(string):
  try:
    result = subprocess.check_output(["magick", "identify", string])
    result_split = str(result).split(' ')
    return result_split[1]
  except:
    return False

def file_extension_matching(file_type, extension_name):
  if file_type == "JPEG" and extension_name == "jpg":
    return True
  elif file_type == "GIF" and extension_name == "gif":
    return True
  elif file_type == "PNG" and extension_name == "png":
    return True
  else:
    return False

cookie = cookies.create_cookies()
session_id = cookies.retrieve_cookies(cookie, 'session')

if session_id == False:
  html_header()
  html_error("Please Login")
  html_tail()

else:
  html_extend_cookies(session_id, cookie)
  form = cgi.FieldStorage()

  # Get filename here.
  fileitem = form['filename']
  upload_mode = form.getvalue('upload-mode')

  # Test if the file was uploaded
  if fileitem.filename:
    filename_split = fileitem.filename.rsplit('.', 1)

    # invalid file name
    if not regex_checking(filename_split[0]):
      html_header()
      html_error("Invalid file name")
      html_tail()

    else:
      # invalid file extension name
      if not check_file_extension_name(fileitem.filename):
        html_header()
        html_error("Invalid file extension name")
        html_tail()
      
      else:
        if not os.path.exists('./tmp/'):
          os.makedirs('./tmp/')
        # strip leading path from file name to avoid directory traversal attacks
        fn = uuid.uuid4().hex + '_' + os.path.basename(fileitem.filename)
        open('./tmp/' + fn, 'wb').write(fileitem.file.read())
        file_type = retrieve_file_type('./tmp/' + fn)

        # change the exif orientation value to prevent image rotated problem
        subprocess.run(["magick", "convert", './tmp/' + fn, "-auto-orient", './tmp/' + fn])

        if (file_type == "JPEG") or (file_type == "GIF") or (file_type == "PNG"):
          if file_extension_matching(file_type, filename_split[1]):
            cookies.set_cookies(cookie, 'upload-mode', upload_mode)
            cookies.set_cookies(cookie, 'image', fn)
            cookies.cookies_head(cookie)
            html_header()
            print("""
            <meta http-equiv="refresh" content="0; url=/cgi-bin/edit.py"/>
            """)
            html_tail()

          else:
            # delete image
            os.remove('./tmp/' + fn)

            html_header()
            html_error("Invalid file content")
            html_tail()

        else:
          # delete image
          os.remove('./tmp/' + fn)

          html_header()
          html_error("Invalid file content")
          html_tail()

  else:
    html_header()
    html_error("No file was uploaded")
    html_tail()
