from copy import copy, deepcopy
import time
from heuristique import *
import Queue

FACTOR = 0

class Node():
        def __init__(self, parent=None, taquin=None):
                # case precedente
                self.parent = parent
		# map du taquin
		self.map = taquin
                # distance depuis le depart
                self.g = 0
                # heirstique
                self.h = 0
                # g + h
                self.f = 0

	# transform la map actuel en string
	def map_str(self):
		string = ""
		for y in range(0, len(self.map)):
			for x in range(0, len(self.map[0])):
				string += str(self.map[y][x])
		return (string)

        def __str__(self):
                return ("pos : " + str(self.map) + " | g : " + str(self.g) + " | h : " + str(self.h) + " | f : " + str(self.f))

def map_str(map):
	string = ""
	for y in range(0, len(map)):
		for x in range(0, len(map[0])):
			string += str(map[y][x])
	return (string)

# parametrer notre resolution de taquin
# heurisitique : fonction eurisdtique que l'ion vuet utiliser
# dim : dfimension de la matrice a traiter
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
		# matrice initial
		self.map = map

	# h : fonction heuristique
	def set_heuristique(self, h):
		self.heuristique = h

	def set_dim(self, dim):
		self.dim = dim

	def set_goal(self, goal):
		self.goal = goal

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

#astar(ori, taquin)
def astar_start(goal, taquin, heuristique=check_hamming):
        # tableau de 4 element qui 
        # initialisation des data
        start_node = Node(None, taquin)
	goal_str = map_str(goal)
        # permet e checker les voisiin par simple addition de pos via une boucle
        neightbours = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # initialisation des liste de priorite
        # noeud a analiser
        open_list = []
        # neud deja analize
        closed_list = []

	# utiliser comme un tableau associatif
	# on stoque ici la stirng de la map de taquin comme une emprinte
	# plus besoin de closed list
	hash = dict()

	# queue bitch:
	q = Queue.PriorityQueue(0)

        # ici on store le premier noeud qui a un cout dez zero
        #open_list.append(start_node)
	q.put((1, start_node))
	hash[start_node.map_str()] = '1'
        # algo:
        # pop open list
        # gen neightbours withtout in closedlist
        # add g, h, f
        finish = 0
	while q.qsize() and finish is 0:
		data = (q.get())[1] # ici opn recupere l object

		#########################################
		# NEW SON GENERATION
                # recuperer la position dwe l empty node
		pos = check_pos_empty(data.map)
                for i in neightbours:
			# ici c est edusewap pas de la simple recuperation de position
			# on va comme meme verifier aue le sposition sont admssible
                        pos_y = pos[0] + i[0]
                        pos_x = pos[1] + i[1]
                        # checker si notre noeud actuel n est pas dans la closed list
                        #if check_pos_is_present((pos_y, pos_x), closed_list) == 0:
                        # checker si on est encore dans le range
                        if pos_x >= 0 and pos_y >= 0 and pos_x < len(data.map[0]) and pos_y < len(data.map):
				new_matrice = deepcopy(data.map)
				# swap value
				#penser a faire la verificatipn de non duplication de notrw list
				new_matrice[pos[0]][pos[1]] = new_matrice[pos_y][pos_x]
				new_matrice[pos_y][pos_x] = 0
				#print (new_matrice)

				# cheker si la nouvelle matrice nexiste pas deja dnas la closed list ou l open list
				newnode = Node(data, new_matrice)
				if (newnode.map_str() not in hash):
                                        # calculer le g h and f
                                        newnode.g = data.g + FACTOR
                                        # newnode.h = check_hamming(new_matrice, goal)#euristique(newnode.pos, end)
                                        # newnode.h = check_manhattan(new_matrice, goal)
                                        #newnode.h = check_hamming(new_matrice, goal)
					newnode.h = heuristique(new_matrice, goal)
                                        newnode.f = newnode.g + newnode.h
                                        #open_list.append(newnode)
					q.put((newnode.f, newnode))
					hash[newnode.map_str()] = '1'

		#######################################################
                # add dans la closed list the father node
                # si on arrive sur la target alors reconstituer le chemin
                # end condition

                # END CONDITION
		if goal_str in hash:
                        data = (q.get())[1]
			print ("need to be 0 : " + str(data.f))
                        finish = 1

	############################################################################

        answer = []
        while (data != None):
                try:
                        answer.append(data.map)
                        data = data.parent
                except:
                        print ("end bitch")
	print("Len path : " + str(len(answer)) + " | Closed list : " + str(len(hash) - (q.qsize() + 1)) + " | Open list : " + str(q.qsize() + 1))
        return (answer)

# heuristique : heuristique function
# map of origin
# dim : dimension of the taquin
def astar_setting(heuristique, map, dim):
	taquin = Taquin(heuristique, dim, 0, map)
	if (dim == 3):
		taquin.set_goal([[1,2,3],[8,0,4],[7,6,5]])
	return (taquin)

# heuristique : heuristique function
# map of origin
# dim : dimension of the taquin
def astar_launch(heuristique, taquin, dim):
	Astar = astar_setting(heuristique, taquin, dim)
	path =  astar_start(Astar.goal, Astar.map, Astar.heuristique)
	return (path)

def main():
	id_line = {}
	goal = [[1,2,3], [8,0,4], [7,6,5]]
	taquin = [[4,8,3], [5,7,2], [0,1,6]]#[[,,], [,,], [,,]]
	#taquin = [[1,2,3], [4,5,6], [7,0,8]]
	#taquin = [[1, 5, 2], [3, 5, 7], [6, 8, 0]]

	path = astar_launch(check_hamming, taquin, 3)
	path = path[::-1]
	print (path)

if __name__ == '__main__':
	start_time = time.time()
        main()
	print("--- %s seconds ---" % (time.time() - start_time))
