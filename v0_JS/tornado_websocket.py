# !/usr/bin/python3
import os
import json
import tornado.web
import tornado.websocket
import tornado.ioloop
from algo_src.a_star import astar_launch
from algo_src.heuristique import check_gaschnig


def first_launch():
	taquin_map = [[7,5,0], [2 ,3 ,8], [4 ,6 ,1]]

	# goal = [[1, 2, 3],[8 ,0 ,4],[7, 6 ,5]]
	
	dico = astar_launch(check_gaschnig, taquin_map, 3, 1)
	print(str(dico))
	return json.dumps(dico)

uri = os.getenv("WS_HOST", "127.0.0.1")
port = os.getenv("WS_PORT", "8082")
address = "ws://" + uri + ":" + port
root = os.path.dirname(__file__)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	connections = set()

	def check_origin(self, origin):
		return True

	def open(self):
		self.connections.add(self)
		print("New client connected")
		self.write_message(first_launch())
		# TODO lancer un n_puzzle de 3 par 3 simple sur l'ouverture
		# afin que l'interface s'ouvre deja sur une solution
	

	def on_message(self, message):
		print("Transmitting message: %s" % message)
		# Gestion de message 
		# FRONT --> BACK
		# FORMAT JSON
		# {
		# }
		#
		print(self.connections)
		for c in self.connections:
			# Euh normalement, il n'y aura qu'un seul et meme client 
			# TODO faut t'il se prendre la tete a gerer de multiples connections ?

			# Il va falloir la en fonction du message lancer A_star avec les bons arguments
			c.write_message(first_launch())

	def on_close(self):
		self.connections.remove(self)
		print("Client disconnected")

print("URI ws://%s:%s is now open for web communication" % (uri, port))
application = tornado.web.Application([
	(r"/", WebSocketHandler)
])
 
if __name__ == "__main__":
	application.listen(8082)
	tornado.ioloop.IOLoop.instance().start()
