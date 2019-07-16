# !/usr/bin/python3
# coding: utf8
import os
import json
import tornado.web
import tornado.websocket
import tornado.ioloop
from algo_src.a_star import astar_launch
from algo_src.utils import spiral, validate_random_puzzle
from algo_src.heuristique import check_gaschnig, check_manhattan, check_hamming


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

	def on_message(self, message):
		print("Transmitting message: %s" % message)

		front_msg = json.loads(message)
		message_send = {}

		print("DEBUG", front_msg)

		if ('algo' in front_msg.keys()):
			puzzle = front_msg['algo']['puzzle']
			if front_msg['algo']['heuristics'] == "manhattan":
				heuristics = check_manhattan
			elif front_msg['algo']['heuristics'] == "gaschnig":
				heuristics = check_gaschnig
			elif front_msg['algo']['heuristics'] == "hamming":
				heuristics = check_hamming
			factor = int(front_msg['algo']['factor'])
			size_puzzle = int(front_msg['algo']['size_puzzle'])
			message_send['algo'] = astar_launch(heuristics, puzzle, size_puzzle, factor)
		elif('random_puzzle' in front_msg.keys()):
			size_puzzle = front_msg['random_puzzle']
			message_send['random_puzzle'] = {}
			message_send['random_puzzle']['puzzle'] = validate_random_puzzle(int(size_puzzle))
			message_send['random_puzzle']['size_puzzle'] = size_puzzle

		elif('logs' in front_msg.keys()):
			print("Client send logs: %s" % front_msg['logs'])
			return 

		if bool(message_send) == False:
			message_send['logs'] = "Error Message Socket invalid"

		print("Message send to a client: %s" % str(message_send))
		self.write_message(json.dumps(message_send))

	def on_close(self):
		self.connections.remove(self)
		print("Client disconnected")

print("URI ws://%s:%s is now open for web communication" % (uri, port))
application = tornado.web.Application([(r"/", WebSocketHandler)], debug=False)
 
if __name__ == "__main__":
	application.listen(8082)
	tornado.ioloop.IOLoop.instance().start()
