# !/usr/bin/python3

# file to launch the file server


import http.server
import socketserver
import os

port = 8080

# launch the file server with the path: 
path = 'interface_src'
web_dir = os.path.join(os.path.dirname(__file__), path)
os.chdir(web_dir)

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", port), Handler)
print("Serving local files at localhost: %d" % port)
httpd.serve_forever()
