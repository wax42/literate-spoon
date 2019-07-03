# !/usr/bin/python3
import os
import json
import tornado.web
import tornado.websocket
import tornado.ioloop
from algo_src.a_star import astar_launch, is_solvable
from algo_src.heuristique import check_gaschnig

# TO DELETE FOR THE TEST	
taquin_map = [[7,5,0], [2 ,3 ,8], [4 ,6 ,1]]

def first_launch():
	
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
		""" Is not important for this local project"""
		return True

	def open(self):
		self.connections.add(self)
		print("New client connected")
		self.write_message(first_launch())
		# TODO lancer un n_puzzle de 3 par 3 simple sur l'ouverture
		# afin que l'interface s'ouvre deja sur une solution
	

	def on_message(self, message):

		"""
		Gestion de message 
		FRONT <--> BACK
		Meme au format au niveau des clés

		0 Astar with parameters
		1 Validate puzzle
		2 Loading size closed size opened
		3 Basic log communication
		message = {
			"algo": {
				"heuristique": "",
				"puzzle": "",
				"size_puzzle": "",
				"factor": "",

			},
			"validate_puzzle": {
				"puzzle": "",
			},
			"stats": {
				"open": "",
				"close" "",
				"all_node": ""
			}
			"logs": {
			}
		}
		"""
		print("Transmitting message: %s" % message)

		front_msg = json.loads(message)
		message_send = {}

		print("DEBUG", front_msg)

		if ('algo' in front_msg.keys()):
			# Launch A star with params
			# param heuristique, puzzle, size_puzzle, factor
			message_send['algo'] = astar_launch(check_gaschnig, taquin_map, 3, 1)
		elif ('validate_puzzle' in front_msg.keys()):
			message_send['validate_puzzle'] = is_solvable(front_msg['validate_puzzle']['puzzle'], len(front_msg['validate_puzzle']['puzzle'])) # TODO don't calculate the len
		elif ('stats' in front_msg.keys()):
			# Chinoiserie pour la fin 
			pass
		elif('logs' in front_msg.keys()):
			# Print msg send by the front
			print("Client send logs: %s" % front_msg['logs'])

		# Gestion de retours et de logs d'erreur
		# 0 result a_star
		# 1 result is_valid puzzle
		# 2 error with the message of errors
		
		# if message send is empty / so the front_message is invalid
		if bool(message_send) == False:
			message_send['logs'] = "Error Message Socket invalid"

		print("Message send to a client: %s" % str(message_send))
		self.write_message(str(message_send))

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
