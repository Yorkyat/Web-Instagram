#! /usr/bin/env python3

import http.cookies
import os
import string
import random
import sqlite3

# create cookies
def create_cookies():
    return http.cookies.SimpleCookie()

# set cookies
def set_cookies(cookies, value):
    cookies['session'] = value
    cookies['session']['expires'] = 1*1*3*60*60

# print cookies header
def cookies_head(cookies):
    print(cookies)

# extend cookies
def cookies_extend(cookies):
    # check cookies exist
    if retrieve_cookies(cookies):
        cookies['session']['expires'] = 1*1*3*60*60

# retrieve cookies
def retrieve_cookies(cookies):
    if 'HTTP_COOKIE' in os.environ:
        cookie_string=os.environ.get('HTTP_COOKIE')
        cookies.load(cookie_string)

    try:
        data = cookies['session'].value
        return data
    except KeyError:
        return False

# delete cookies
def del_cookies(cookies):
    cookies['session']=''
    cookies['session']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'

# generate random string
def id_generator(size=128, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# check table exist
def check_session_table_exist(c):
    sql = "CREATE TABLE IF NOT EXISTS `session` (`username` TEXT NOT NULL UNIQUE, `session_id` TEXT UNIQUE)"
    c.execute(sql)

# set session id
def set_session_id(username, c, conn):
    session_id = id_generator()
    check_session_table_exist(c)
    sql = "INSERT OR REPLACE INTO `session` (`username`, `session_id`) VALUES (?,?)"
    c.execute(sql, (username, session_id,))
    conn.commit()
    return session_id

# delete session id
def del_session_id(session_id, c, conn):
    check_session_table_exist(c)
    sql = "DELETE FROM `session` WHERE `session_id` = ?"
    c.execute(sql, (session_id,))
    conn.commit()

# retrieve username
def retrieve_username(session_id):
    conn = sqlite3.connect('../index.db')
    cursor = conn.cursor()
    check_session_table_exist(cursor)
    sql = "SELECT `username` FROM `session` WHERE `session_id` = ?;"
    cursor.execute(sql, (session_id,))
    data = cursor.fetchone()
    username = data[0]
    conn.close()
    return username

