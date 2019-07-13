from .utils import map_str, check_pos_empty, spiral, is_solvable
from copy import deepcopy
import heapq, time
from .heuristique import *

class Taquin():
	def __init__(self, heuristique, dim, goal, map):
		# fonction euristique aue l on va utiliser
		self.heuristique = heuristique
		# dimension de la matrice
		self.dim = dim
		# matrice cible
		self.goal = goal

		self.goal1d = []

		# matrice initial
		self.map = map

		self.factor = 0

		# 1 : taquin unsolvable
		# 2 : invalid dim
		self.error = 0

		# stats part
		self.len_path    = 0
		self.nb_all_node = 0
		self.nb_open = 0

	# h : fonction heuristique
	def set_heuristique(self, h):
		self.heuristique = h

	def set_dim(self, dim):
		self.dim = dim

	def set_goal(self, goal):
		self.goal = goal
		self.goal1d = []
		for i in self.goal:
			self.goal1d += i

	def set_map(self, map):
		self.map = map

class Node():
	def __init__(self, parent=None, taquin=None):
			self.parent = parent

			self.map = taquin

			self.g = 0
			# g + h
			self.f = 0

#	# transform la map actuel en string
	def map_str(self, dim):
		string = ""
		for y in range(0, dim):
			for x in range(0, dim):
				string += str(self.map[y][x])
		return (string)

	def __lt__(self, other):
		return self.f < other.f

	def __eq__(self, other):
		if(other == None):
			return False
		return self.f == other.f


def astar_start(taquin):
	start_node = Node(None, taquin.map)
	goal_str = map_str(taquin.goal, taquin.dim)

	neightbours = [(0, -1), (0, 1), (-1, 0), (1, 0)]
	total =  0 # TODO delete the queue and count the total of node here

	closed_list = set()

	opened_list = []

	heapq.heappush(opened_list, (1, start_node))
	taquin.nb_all_node += 1

	# we store just the key not a value
	closed_list.add(start_node.map_str(taquin.dim))

	while len(opened_list):
		data = (heapq.heappop(opened_list))[1]
		pos = check_pos_empty(data.map)
		for i in neightbours:
			pos_y = pos[0] + i[0]
			pos_x = pos[1] + i[1]
			if pos_x >= 0 and pos_y >= 0 and pos_x < taquin.dim and pos_y < taquin.dim:
				new_matrice = deepcopy(data.map)
				new_matrice[pos[0]][pos[1]] = new_matrice[pos_y][pos_x]
				new_matrice[pos_y][pos_x] = 0

				newnode = Node(data, new_matrice)
				newnode_map_str = newnode.map_str(taquin.dim)

				if newnode_map_str not in closed_list:
					newnode.g = data.g + taquin.factor
					newnode.h = taquin.heuristique(new_matrice, taquin.goal1d)
					heapq.heappush(opened_list, (newnode.g + newnode.h, newnode))
					closed_list.add(newnode_map_str)
					taquin.nb_all_node += 1
					if (newnode_map_str == goal_str):
						path = []
						node_actual = newnode
						while (node_actual != None):
							try:
								path.append(node_actual.map)
								node_actual = node_actual.parent
							except:
								print ("***")
						taquin.len_path = len(path)
						taquin.nb_open = len(opened_list)
						path = path[::-1]
						return (path)
	return (-1)

# heuristique : heuristique function
# map of origin
# dim : dimension of the taquin
def astar_setting(heuristique, map, dim):
	taquin = Taquin(heuristique, dim, 0, map)
	if (dim >= 3 and dim <= 10):
		taquin.set_goal(spiral(dim))
	else:
		taquin.error = 2

	if (is_solvable(taquin.map, taquin.goal, dim) == 0):
		taquin.error = 1

	return (taquin)

# heuristique : heuristique function
# map of origin
# dim : dimension of the taquin
def astar_launch(heuristique, taquin, dim, factor=0):
	
	Astar = astar_setting(heuristique, taquin, dim)
	Astar.factor = factor
	if (Astar.error == 1):
		print("Taquin invalide. Try another file.")
		exit(1) # TODO delete the exit
	if (Astar.error == 2):
		print ("Bad dim. Need to be [2 < dim < 6]")
		exit(1) # TODO delete the exit

	start_time = time.time()
	path = astar_start(Astar)
	time_duration = time.time() - start_time
	print ("*********************************")
	print ("************* PATH *************")
	print (path)

	# STATS DISPLAYIN
	print ("*********************************")
	print ("************* STATS *************")
	print ("DIMENSION     : " + str(dim) + " * " + str(dim))
	print ("LEN PATH      : " + str(Astar.len_path))
	print ("NB NODE OPEN  : " + str(Astar.nb_all_node))
	print ("NB OPEN       : " + str(Astar.nb_open))
	print ("NB CLOSE      : " + str((Astar.nb_all_node - Astar.nb_open)))
	print ("TIME DURATION : %.3f" % time_duration)

	send_dico = {}
	send_dico['path'] = path
	send_dico['size_puzzle'] = dim
	send_dico['len_path'] = Astar.len_path
	send_dico['all_node'] = Astar.nb_all_node
	send_dico['node_open'] = Astar.nb_open
	send_dico['node_close'] = Astar.nb_all_node - Astar.nb_open
	send_dico['time_duration'] = str(time_duration)

	return (send_dico)
