#! /usr/bin/env python3
header = "Content-Type: text/html\r\n"
html = """
<html>
<body>
<a href="/cgi-bin/login.py">Login</a>
<a href="/cgi-bin/signup.py">Sign Up</a>
<a href="/cgi-bin/changepw.py">Change Password</a>
</body>
</html>
"""
print(header+html)