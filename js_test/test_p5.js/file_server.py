# !/usr/bin/python3
import http.server
import socketserver

port = 8080

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", port), Handler)
print("Serving local files at localhost: %d" % port)
httpd.serve_forever()
