#! /usr/bin/env python3

import cgi, cgitb
import os
import sqlite3
import cookies
import subprocess
import platform

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

def html_image(image):
    print("""
    <div class="container text-center my-3">
        <img style="max-height: 1000px; max-width: 1000px; width: auto; height: auto" src={0}>
    </div>
    """.format("/tmp/" + image))

def html_filter(parameter):
    if parameter == None:
        parameter = ""
    
    print("""
    <form action = "/cgi-bin/edit.py" method = "get">
      <div class="container text-center my-5">
        <span class="mx-5">Filters</span>
        <a href="/cgi-bin/edit.py?filter={0}"><button type="button" class="btn btn-primary mx-2">Filter 1</button></a>
        <a href="/cgi-bin/edit.py?filter={1}"><button type="button" class="btn btn-primary mx-2">Filter 2</button></a>
        <a href="/cgi-bin/edit.py?filter={2}"><button type="button" class="btn btn-primary mx-2">Filter 3</button></a>
        <a href="/cgi-bin/edit.py?filter={3}"><button type="button" class="btn btn-primary mx-2">Filter 4</button></a>
        <a href="/cgi-bin/edit.py?filter={4}"><button type="button" class="btn btn-primary mx-2">Filter 5</button></a>
      </div>
    </form>
    <hr>
    """.format(parameter+"%1", parameter+"%2", parameter+"%3", parameter+"%4", parameter+"%5"))

def html_option(parameter):
    print("""
    <form action "/cgi-bin/edit.py" method = "post">
      <div class="container text-right my-3">
    """)

    if parameter != None:
        parameter_split = parameter.rsplit('%', 1)
        if parameter_split[0] == "":
            print("""
                <a href="/cgi-bin/edit.py"><button type="button" class="btn btn-primary mx-1">Undo</button></a>        
            """)
        else:
            print("""
                <a href="/cgi-bin/edit.py?filter={0}"><button type="button" class="btn btn-primary mx-1">Undo</button></a>        
            """.format(parameter_split[0]))
    else:
        print("""
        <button type="button" class="btn btn-primary mx-1" disabled>Undo</button>       
        """)

    print("""
        <input class="btn btn-primary mx-1" type = "submit" name = "option" value = "Discard" />
        <input class="btn btn-primary mx-1" type = "submit" name = "option" value = "Finish" />    
      </div>
    </form>
    """)

def html_extend_cookies(session_id, upload_mode, image, cookie):
    if session_id:
        cookies.cookies_extend(cookie, 'session')
        cookies.cookies_head(cookie)
    if upload_mode:
        cookies.cookies_extend(cookie, 'upload-mode')
        cookies.cookies_head(cookie)
    if image:
        cookies.cookies_extend(cookie, 'image')
        cookies.cookies_head(cookie)

def check_img_table_exist(c):
    sql = "CREATE TABLE IF NOT EXISTS 'image'(`pid` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,`image` TEXT NOT NULL UNIQUE,`mode` TEXT NOT NULL,`username` TEXT,`timestamp` TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
    c.execute(sql)

def remove_tmp_images():
    if os.path.exists("./tmp/" + image):
        os.remove("./tmp/" + image)
    if os.path.exists("./tmp/" + '1_' + image):
        os.remove("./tmp/" + '1_' + image)
    if os.path.exists("./tmp/" + '2_' + image):
        os.remove("./tmp/" + '2_' + image)
    if os.path.exists("./tmp/" + '3_' + image):
        os.remove("./tmp/" + '3_' + image)
    if os.path.exists("./tmp/" + '4_' + image):
        os.remove("./tmp/" + '4_' + image)
    if os.path.exists("./tmp/" + '5_' + image):
        os.remove("./tmp/" + '5_' + image)
    if os.path.exists("./tmp/" + 'itm_4_' + image):
        os.remove("./tmp/" + 'itm_4_' + image)
    if os.path.exists("./tmp/" + 'tmp_3_' + image):
        os.remove("./tmp/" + 'tmp_3_' + image)
    if os.path.exists("./tmp/" + 'tmp_4_' + image):
        os.remove("./tmp/" + 'tmp_4_' + image)


if not os.path.exists('./tmp/'):
    os.makedirs('./tmp/')

form = cgi.FieldStorage() 

cookie = cookies.create_cookies()
session_id = cookies.retrieve_cookies(cookie, 'session')
upload_mode = cookies.retrieve_cookies(cookie, 'upload-mode')
image = cookies.retrieve_cookies(cookie, 'image')
resolution = ""
height = ""
width = ""

if (session_id == False) or (upload_mode == False) or (image == False):
  html_header()
  print("""<meta http-equiv="refresh" content="0; url=/cgi-bin/index.py"/>""")
  html_tail()

else:
    username = cookies.retrieve_username(session_id)
    html_extend_cookies(session_id, upload_mode, image, cookie)
    if "option" in form:
        option = form.getvalue('option')
        if "filter" not in form:
            filter_apply = None
        else:
            filter_parameter = form.getvalue('filter')
            filter = filter_parameter.rsplit('%', 1)
            filter_apply = filter[1]

        if option == "Discard":
            # remove all used stuff
            cookies.del_cookies(cookie, 'upload-mode')
            cookies.del_cookies(cookie, 'image')
            remove_tmp_images()

            cookies.cookies_head(cookie)
            html_header()
            print("""<meta http-equiv="refresh" content="0; url=/cgi-bin/index.py"/>""")
            html_tail()
            
        elif option == "Finish":
            if filter_apply == None:
                os.rename("./tmp/" + image, "./img/" + image)
            else:
                os.rename("./tmp/" + filter_apply + '_' + image, "./img/" + image)

            conn = sqlite3.connect('../index.db')
            cursor = conn.cursor()
            check_img_table_exist(cursor)
            if upload_mode == "public":
                sql = "INSERT INTO `image` (`image`,`mode`) VALUES (?,?)"
                cursor.execute(sql, (image, upload_mode,))
                conn.commit()
            else:
                sql = "INSERT INTO `image` (`image`,`mode`,`username`) VALUES (?,?,?)"
                cursor.execute(sql, (image, upload_mode, username,))
                conn.commit()
            conn.close()

            # remove all used stuff
            cookies.del_cookies(cookie, 'upload-mode')
            cookies.del_cookies(cookie, 'image')
            remove_tmp_images()
            cookies.cookies_head(cookie)
            html_header()
            path = os.environ['HTTP_REFERER']
            host = path.rsplit('/', 2)[0]
            permalink = host + '/img/' + image
            print("""<h1>Success</h1>
                    <p>Upload success</p>
                    <div class="container text-center my-3">
                        <img style="max-height: 1000px; max-width: 1000px; width: auto; height: auto" src={0}>
                        <a href={1}><span>{1}</span></a>
                    </div>
                    <div class="container text-right">
                        <a href="/cgi-bin/index.py"><button type="button" class="btn btn-primary mx-3 text-right">Back to Index Page</button></a>
                    </div>
                    """.format("/img/" + image, permalink))
            html_tail()
        
        # assume having unexpected error
        else:
            print("""<meta http-equiv="refresh" content="0; url=/cgi-bin/edit.py" />""")

    else:
        if "filter" not in form:
            filter_parameter = None
            filter_apply = None
        else:   
            filter_parameter = form.getvalue('filter')
            filter = filter_parameter.rsplit('%', 1)
            filter_apply = filter[1]
            result = subprocess.check_output(["magick", "identify", "./tmp/" + image])
            resolution = str(result).split(' ')[2]
            height = resolution.split('x')[0]
            width = resolution.split('x')[1]

            if filter_apply == "1":
                subprocess.run(["magick", "convert", "./tmp/" + image, "-bordercolor", "black", "-border", "25", "./tmp/" + "1_" + image])
                image = "1_" + image
            elif filter_apply == "2":
                subprocess.run(["magick", "convert", "./tmp/" + image, "-channel", "R", "-level", "33%", "-channel", "G", "-level", "33%", "./tmp/" + "2_" + image])
                image = "2_" + image
            elif filter_apply == "3":
                subprocess.run(["magick", "convert", "./lensflare.png", "-resize", width + 'x', "./tmp/" + "tmp_3_" + image])
                subprocess.run(["magick", "composite", "-compose", "screen", "-gravity", "northwest", "./tmp/" + "tmp_3_" + image, "./tmp/" + image, "./tmp/" + "3_" + image])
                image = "3_" + image
            elif filter_apply == "4":
                subprocess.run(["magick", "convert", "./tmp/" + image, "-type", "grayscale", "./tmp/" + "itm_4_" + image])
                subprocess.run(["magick", "convert", "./bwgrad.png", "-resize", height + 'x' + width + "!", "./tmp/" + "tmp_4_" + image])
                subprocess.run(["magick", "composite", "-compose", "softlight", "-gravity", "center", "./tmp/" + "tmp_4_" + image, "./tmp/" + "itm_4_" + image, "./tmp/" + "4_" + image])
                image = "4_" + image

            elif filter_apply == "5":
                subprocess.run(["magick", "convert", "./tmp/" + image, "-blur", "0.5x2", "./tmp/" + "5_" + image])
                image = "5_" + image
        html_header()
        html_image(image)
        html_filter(filter_parameter)
        html_option(filter_parameter)   
        html_tail()
