# !/usr/bin/python3
import os
import tornado.web
import tornado.websocket
import tornado.ioloop

uri = os.getenv("WS_HOST", "127.0.0.1")
port = os.getenv("WS_PORT", "8082")
address = "ws://" + uri + ":" + port
root = os.path.dirname(__file__)
# class MainHandler(tornado.web.RequestHandler):
# 	def get(self):
# 		# items = ["Item 1", "Item 2", "Item 3"]
# 		self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	connections = set()

	def check_origin(self, origin):
		return True

	def open(self):
		self.connections.add(self)
		print("New client connected")
		self.write_message("You are connected")

	def on_message(self, message):
		print("Transmitting message: %s" % message)
		for c in self.connections:
			c.write_message(message)

	def on_close(self):
		self.connections.remove(self)
		print("Client disconnected")

print("URI ws://%s:%s is now open for web communication" % (uri, port))
application = tornado.web.Application([
	# (r"/(.*)", tornadso.web.StaticFileHandler, {"path": root, "default_filename": "index.html"}),
	# (r"/", MainHandler),
	(r"/", WebSocketHandler),
])
 
if __name__ == "__main__":
	application.listen(8082)
	tornado.ioloop.IOLoop.instance().start()
