#! /usr/bin/env python3
header = "Content-Type: text/html\r\n"

html = """
<!DOCTYPE html>
<html>
<head>
<link type="text/css" rel="stylesheet" href="/changepw.css" />
</head>
<div class="container">
    <h1>Change Password</h1>
    <hr>

    <label><b>Current Password</b></label>
    <input type="text" placeholder="Enter Current Password" name="password-old" required>

    <label><b>New Password</b></label>
    <input type="password" placeholder="Enter New Password" name="password-new" required>

    <label><b>Retype New Password</b></label>
    <input type="password" placeholder="Retype New Password" name="password-retype" required>

    <div class="clearfix">
      <button type="button" class="cancelbtn">Cancel</button>
      <button type="submit" class="updatebtn">Update</button>
    </div>
</div>
"""
print(header + html)
