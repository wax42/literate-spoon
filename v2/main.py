import time
import heapq
import argparse
import ui_v2
import my_argparse
from copy import deepcopy
from heuristique import *

class Node():
	def __init__(self, parent=None, taquin=None):
			# case precedente
			self.parent = parent
			# map du taquin
			self.map = taquin
			# distance depuis le depart
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

def map_str(map, dim):
	string = ""
	for y in range(0, dim):
		for x in range(0, dim):
			string += str(map[y][x])
	return (string)

# parametrer notre resolution de taquin
# heurisitique : fonction heuristique que l'on veut utiliser
# dim : dimension de la matrice a traiter
# goal : pattern final que l'on veut obtenir
# map : tableau a 2 dimension qui represente la map de commencement du taquin
class Taquin():
	def __init__(self, heuristique, dim, goal, map):
		# fonction euristique aue l on va utiliser
		self.heuristique = heuristique
		# dimension de la matrice
		self.dim = dim
		# matrice cible
		self.goal = goal
		self.goal_real = 0
		# matrice initial
		self.map = map

		self.factor = 0

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

	def set_goal_real(self, goal):
		self.goal_real = goal

	def set_map(self, map):
		self.map = map

# toruver la position de l empty element
# find element 0
def check_pos_empty(taquin_map):
	for y in range(0, len(taquin_map)):
		for x in range(0, len(taquin_map[0])):
			if (taquin_map[y][x] == 0):
				return (y, x)
	return (-1, -1)

#def astar_start(goal, taquin, heuristique=check_hamming):
def astar_start(taquin):
	# tableau de 4 element qui 
	# initialisation des data
	start_node = Node(None, taquin.map)
	goal_str = map_str(taquin.goal, taquin.dim)
	# permet e checker les voisiin par simple addition de pos via une boucle
	neightbours = [(0, -1), (0, 1), (-1, 0), (1, 0)]
	total =  0

	# initialisation des liste de priorite

	# utiliser comme un tableau associatif
	# on stoque ici la string de la map de taquin comme une emprinte
	# remplace la closed list
	hash = set()

	# queue bitch:
	pqueue = []

        # ici on store le premier noeud qui a un cout dez zero
	heapq.heappush(pqueue, (1, start_node))
	taquin.nb_all_node += 1
	# we store just the key not a value
	hash.add(start_node.map_str(taquin.dim))
	# algo:
	# pop open list
	# gen neightbours withtout in closedlist
	# add g, h, f
	while len(pqueue):
		data = (heapq.heappop(pqueue))[1] # ici on recupere l object
		#########################################
		# NEW SON GENERATION
                # recuperer la position dwe l empty node
		pos = check_pos_empty(data.map)
		for i in neightbours:
			pos_y = pos[0] + i[0]
			pos_x = pos[1] + i[1]
			# checker si notre noeud actuel n est pas dans la closed list
			# checker si on est encore dans le range
			# pour l opti on va eviter le len
			if pos_x >= 0 and pos_y >= 0 and pos_x < taquin.dim and pos_y < taquin.dim:
				new_matrice = deepcopy(data.map)
				# swap value
				#penser a faire la verification de non duplication de notre list
				new_matrice[pos[0]][pos[1]] = new_matrice[pos_y][pos_x]
				new_matrice[pos_y][pos_x] = 0

				# checker si la nouvelle matrice nexiste pas deja dans la closed list ou l open list
				newnode = Node(data, new_matrice)
				newnode_map_str = newnode.map_str(taquin.dim)
				if (newnode_map_str not in hash):
					# calculer le g h and f
					newnode.g = data.g + taquin.factor
					newnode.h = taquin.heuristique(new_matrice, taquin.goal)
					heapq.heappush(pqueue, (newnode.g + newnode.h, newnode))
					hash.add(newnode_map_str)
					taquin.nb_all_node += 1

		#######################################################
                # add dans la closed list the father node
                # si on arrive sur la target alors reconstituer le chemin
                # end condition

                # END CONDITION
		if goal_str in hash:
			data = (heapq.heappop(pqueue))[1]
			break

	############################################################################
	### Build path
	answer = []
	while (data != None):
			try:
					answer.append(data.map)
					data = data.parent
			except:
					print ("end bitch")
	taquin.len_path = len(answer)
	taquin.nb_open = len(pqueue)
	return (answer)

# heuristique : heuristique function
# map of origin
# dim : dimension of the taquin
def find_pos_in_tab(tab, val):
	count = 0
	print ("find " + str(val) + " in " + str(tab))
	for i in tab:
		if (i == val):
			print ("\tValue found : " + str(count))
			return (count)
		count += 1

# find n  number a > b 7 a != 0 b != 0
def find_n(map_no_stair):
	size = len(map_no_stair)
	n = 0
	for x in range(0, size):
		for y in range(x+1, size):
			if (map_no_stair[x] != 0 and map_no_stair[y] != 0 and map_no_stair[x] > map_no_stair[y]):
				n += 1
	return (n)

def astar_setting(heuristique, map, dim):
	taquin = Taquin(heuristique, dim, 0, map)
	if (dim == 3):
		taquin.set_goal([[1, 2, 3],[8 ,0 ,4],[7, 6 ,5]])
		taquin.set_goal_real([1, 2, 3, 4, 0, 5, 6, 7 ,8])
	elif (dim == 4):
		taquin.set_goal([[1, 2, 3, 4], [12, 13, 14, 5], [11, 0, 15, 6], [10, 9, 8, 7]])
		taquin.set_goal_real([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 10, 11, 12, 13, 14, 15])
	elif (dim == 5):
		taquin.set_goal([[1, 2, 3, 4, 5], [16, 17, 18, 19, 6], [15, 24, 0, 20, 7], [14, 23, 22, 21, 8], [13, 12, 11, 10, 9]])
		taquin.set_goal_real([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])

	#verifier que l on peut resoudre le taquin
#	count_diff = 0
#	for y in range(0, dim):
#		for x in range(0, dim):
#			if (taquin.map[y][x] != taquin.goal[y][x]):
#				count_diff += 1	
	# TAQUIN VERIF SOLVABLE

	print ("MAT1")
	print (taquin.map)
	print ("MAT2")
	print (taquin.goal)

	tab_map = []
	tab_goal = []

	tab_final = []
	zero_empl = 0

	for i in taquin.map:
		tab_map = tab_map + i
	for i in taquin.goal:
		tab_goal = tab_goal + i
	
	size = len(tab_map)
	# build tab pos
	for i in range(0, size):
		tab_final.append(find_pos_in_tab(tab_goal, tab_map[i]))
	

	print ("MAP input             : " + str(tab_map))
	print ("Goal                  : " + str(tab_goal))
	# 
	print ("tab de correspondance : " + str(tab_final))

	print ("Goal real             : " + str(taquin.goal_real))

	print ("Build dictionnaries of dictionnaries : ")
	dcorrep = dict()

	# construciton de notre tableau de corresponance entre notre matrice en escalier et une matrice sans escalier pour ainsi effectuer l opperation permettant de savoir si c est valide
	for i in range(0, size):
		dcorrep[tab_goal[i]] = taquin.goal_real[i]

	# creation du tableau qui correspond a une matrice sans escalier ;)
	master_mat = []
	for i in tab_map:
		master_mat.append(dcorrep[i])

	print (dcorrep)

	print ("master_map : " + str(master_mat))

	N = find_n(master_mat)
	print ("nb diff : " + str(N))

	if (dim % 2 == 1):
		if (N % 2 == 0):
			print("SOLVABLE")
		else:
			print ("No SOLVABLE")
	else:
		# dans le cas pair
		#
		print (map)
		bottom_y = -1
		for y in range(0, dim):
			for x in range(0, dim):
				if (taquin.map[y][x] == 0):
					bottom_y = dim - y;

		print ("N : " + str(N) + " and bottom_y : " + str(bottom_y))
		if (N % 2 == 0 and bottom_y % 2 == 0):
			print ("UNSOLVABLE N even and y even")
		elif (N % 2 == 1 and bottom_y % 2 == 1):
			print ("UNSOLVABLE N odd and y odd")
		else:
			print ("GOOD SOLVE\n")
		print ("Pos from the bottom : " + str(bottom_y))

		print ("bad solution")
	#exit(1)
	return (taquin)

# heuristique : heuristique function
# map of origin
# dim : dimension of the taquin
def astar_launch(heuristique, taquin, dim, factor=0):
	Astar = astar_setting(heuristique, taquin, dim)
	Astar.factor = factor
	path = astar_start(Astar)
	print ("*********************************")
	print ("************* PATH *************")
	print (path)

	# STATS DISPLAYING
	print ("*********************************")
	print ("************* STATS *************")
	print ("DIMENSION     : " + str(dim) + " * " + str(dim))
	print ("LEN PATH      : " + str(Astar.len_path))
	print ("NB NODE OPEN  : " + str(Astar.nb_all_node))
	print ("NB OPEN       : " + str(Astar.nb_open))
	print ("NB CLOSE      : " + str((Astar.nb_all_node - Astar.nb_open)))
	return (path)

def main(parse):
	id_line = {}
        # parse argument
	print(argparse.__file__)

	parse = my_argparse.parsing_bitch()
	print(parse.matrice)

	path = astar_launch(parse.heuristique, parse.matrice, parse.dim, parse.factor)
	path = path[::-1]
	return (str(path))

if __name__ == '__main__':
	parse = my_argparse.parsing_bitch()
	start_time = time.time()
	path = main(parse)
	print ("SECONDS       : %.3f" % (time.time() - start_time))
	if (parse.graphic):
		ui_v2.graphic_mode(path)
