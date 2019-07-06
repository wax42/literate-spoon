# !/usr/bin/python3
# coding: utf8
import os
import json
import tornado.web
import tornado.websocket
import tornado.ioloop
from algo_src.a_star import astar_launch, is_solvable
from algo_src.utils import spiral, random_puzzle
from algo_src.heuristique import check_gaschnig

# TO DELETE FOR THE TEST	
taquin_map = [[7,5,0], [2 ,3 ,8], [4 ,6 ,1]]

uri = os.getenv("WS_HOST", "127.0.0.1")
port = os.getenv("WS_PORT", "8082")
address = "ws://" + uri + ":" + port
root = os.path.dirname(__file__)


def generate_radom_puzzle(dim):
		goal = spiral(dim)
		solvable = 0
		while (solvable == 0):
			pzl = random_puzzle(dim)
			solvable = is_solvable(pzl, goal, dim)
		return pzl


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	connections = set()

	def check_origin(self, origin):
		""" Is not important for this local project"""
		return True

	def open(self):
		self.connections.add(self)
		print("New client connected")
		message_send = {}
		message_send['algo'] = astar_launch(check_gaschnig, taquin_map, 3, 1)
		# self.write_message(str(message_send))
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
		4 random_puzzle
		message = {
			"algo": {
				"heuristique": "",
				"puzzle": "",
				"size_puzzle": "",
				"factor": "",

			},
			"validate_puzzle": [[]],
			"stats": {
				"open": "",
				"close" "",
				"all_node": ""
			}
			"logs": {
			}
			"random_puzzle" {
				"size_puzzle" = 2;
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
			message_send['algo'] = astar_launch(check_gaschnig, taquin_map, 3, 0)
			# print("QUESECE CE QUE C QU CA", message['algo'])
		elif ('validate_puzzle' in front_msg.keys()):
			# Convert double array of str in double array of int
			size_puzzle = front_msg['validate_puzzle']['size_puzzle']
			puzzle = front_msg['validate_puzzle']['puzzle'] 
			for i in range(size_puzzle):
				puzzle[i] = list(map(int, puzzle[i])) 
			message_send['validate_puzzle'] = is_solvable(puzzle, spiral(size_puzzle), size_puzzle)# TODO don't calculate the len
		# elif ('stats' in front_msg.keys()):
		# 	# Chinoiserie pour la fin 
		# 	pass
		elif('random_puzzle' in front_msg.keys()):
			message_send['random_puzzle'] = generate_radom_puzzle(front_msg["random_puzzle"]["size_puzzle"])

		elif('logs' in front_msg.keys()):
			# Print msg send by the front
			print("Client send logs: %s" % front_msg['logs'])
			message_send['logs'] = "back suck your fucking msg"  # TODO faire un truc intelligent

		# Gestion de retours et de logs d'erreur
		# algo result a_star
		# validate_puzzle result is_valid puzzle
		# logs error with the message of errors
		# stats 

		# if message send is empty / so the front_message is invalid
		if bool(message_send) == False:
			message_send['logs'] = "Error Message Socket invalid"

		print("Message send to a client: %s" % str(message_send))
		self.write_message(json.dumps(message_send))

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
