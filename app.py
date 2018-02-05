#! /usr/bin/env python3

import http.server
import os
import sys

os.chdir('www')
port = 8080

server_address = ('', port)
httpd = http.server.HTTPServer(server_address, http.server.CGIHTTPRequestHandler)

print("Listening Port %d"%port)
httpd.serve_forever()
