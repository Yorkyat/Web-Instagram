#! /usr/bin/env python3
header = "Content-Type: text/html\r\n"

html = """
<!DOCTYPE html>
<html>
<head>
<link type="text/css" rel="stylesheet" href="/login.css" />
</head>
<div class="container">
    <h1>Login</h1>
    <hr>

    <label><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="username" required>

    <label><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="password" required>

    <button type="submit">Login</button>
</div>
</body>
</html>
"""

print(header + html)
