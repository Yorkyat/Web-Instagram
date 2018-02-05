#! /usr/bin/env python3
header = "Content-Type: text/html\r\n"

html = """
<!DOCTYPE html>
<html>
<head>
<link type="text/css" rel="stylesheet" href="/signup.css" />
</head>
<div class="container">
    <h1>Sign Up</h1>
    <hr>

    <label><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="username" required>

    <label><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="password" required>

    <label><b>Retype Password</b></label>
    <input type="password" placeholder="Retype Password" name="password-retype" required>

    <div class="clearfix">
      <button type="button" class="cancelbtn">Cancel</button>
      <button type="submit" class="signupbtn">Sign Up</button>
    </div>
</div>
"""
print(header + html)
