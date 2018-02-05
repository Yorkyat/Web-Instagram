#! /usr/bin/env python3
header = "Content-Type: text/html\r\n"

html = """
<!DOCTYPE html>
<html>
  <div class="container">
    <label><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="uname" required>

    <label><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>

    <button type="submit">Login</button>
    <label>
      <input type="checkbox" checked="checked"> Remember me
    </label>
  </div>
</body>
</html>
"""

print(header+html)
