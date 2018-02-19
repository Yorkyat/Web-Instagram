# Web-Instagram
CSCI 4140 assignment 1

The website on the openshift server: 
- http://web-instagram-web-instagram-york.a3c1.starter-us-west-1.openshiftapps.com

Be careful:
To begin, it will first ask to initialize the system. The admin's username is "Admin" and it will ask to create a password.
After creating the password for the admin account, it will auto-login with the admin account and start the initialization.

Project structure:
- app.py: cgi server
- www: change directory to this folder to prevent the access to the app.py and database
  - cgi-bin: store all cgi files
    - changepw.py: change password page and handle the request of update password
    - cookies.py: functions of cookies
    - edit.py: editor page and handle all requests in editor (filters, undo, discard, finish)
    - index.py: index page and list images
    - init.py: handle all initialize requests
    - init_changepw.py: change admin default password
    - login.py: login page and handle login request
    - logout: handle logout request
    - signup: sign up page and handle sign up request
    - upload: handle upload request
  - img: store image with permalink
  - tmp: store images uploaded and generated in editor
  - bwgrad.png, lensflare.png: used for filters
  - index.html: default html of openshift, redirect to index.py
  - init.html: initialization page
  - changepw.css, login.css, signup.css: css for change password, login and sign up pages
  
Project procedure:
--
Access Control & Session Management is first implemented.
SQLite 3 is used. Create the database and the user, session tables. Finish sign up, then write cookies function, finish login, change password, logout.
Start to implement Index Page & File Upload.
Finish index page, make pagination.
Test upload simple file. Then create image table and finish upload image.
Implement Photo Editor.
Implement the Undo, then implement the filters, discard and finally finsh function.
Implement System Initialization.
Fix some bugs.
Testing and debugs are done when implementing in each part.
