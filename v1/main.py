from copy import copy, deepcopy
import time
from heuristique import *

FACTOR = 0

class Node():
        def __init__(self, parent=None, taquin=None):
                # case precedente
                self.parent = parent
                # pos de notre neud
                #self.pos = pos
		self.map = taquin
                # distance depuis le depart
                self.g = 0
                # heirstique
                self.h = 0

                # g + h
                self.f = 0

        def __eq__(self, other):
                return (self.pos == other.pos)

        def __str__(self):
                return ("pos : " + str(self.map) + " | g : " + str(self.g) + " | h : " + str(self.h) + " | f : " + str(self.f))


def check_same_map(map1, map2):
	xx = len(map1)
	yy = len(map1[0])
	for y in range(0, yy):
		for x in range(0, xx):
			if (map1[y][x] != map2[y][x]):
				return (0)
	return (1)

def check_map_is_present_in_list(map1, l1):
	for i in l1:
		if (check_same_map(map1, i.map) == 1):
			return (1)
	return (0)

def str_list_node(listNode):
        for i in listNode:
                print(listNode)

#def euristique(s1, pts2):
#        return abs(pts1[0] - pts2[0]) + abs(pts1[1] - pts2[1])

# toruver la position de l empty element
# find element 0
def check_pos_empty(taquin_map):
	for y in range(0, len(taquin_map)):
		for x in range(0, len(taquin_map[0])):
			if (taquin_map[y][x] == 0):
				return (y, x)
	return (-1, -1)

#astar(ori, taquin)
def astar(goal, taquin):
        # tableau de 4 element qui 
        # initialisation des data
        start_node = Node(None, taquin)
        # permet e checker les voisiin par simple addition de pos via une boucle
        neightbours = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # initialisation des liste de priorite
        # noeud a analiser
        open_list = []
        # neud deja analize
        closed_list = []

	# dict
	hash = {}

        # ici on store le premier noeud qui a un cout dez zero
        open_list.append(start_node)

        # algo:
        # pop open list
        # gen neightbours withtout in closedlist
        # add g, h, f
        finish = 0
        while len(open_list) and finish is 0:
		print ("Open list : " + str(len(open_list)))
                data = open_list.pop()
                print (" : open list len : " + str(len(open_list)) + " | closed list : " + str(len(closed_list)))
  
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
				print (new_matrice)

				# cheker si la nouvelle matrice nexiste pas deja dnas la closed list ou l open list
				if (check_map_is_present_in_list(new_matrice, open_list) == 0 and check_map_is_present_in_list(new_matrice, closed_list) == 0):
					newnode = Node(data, new_matrice)
                                        # calculer le g h and f
                                        newnode.g = data.g + FACTOR
                                        # newnode.h = check_hamming(new_matrice, goal)#euristique(newnode.pos, end)
                                        # newnode.h = check_manhattan(new_matrice, goal)
                                        newnode.h = check_hamming(new_matrice, goal)
                                        newnode.f = newnode.g + newnode.h
                                        open_list.append(newnode)
					print ("New node\n")
					#return "coucou"
		
		open_list.sort(key=lambda Node : Node.f, reverse=True)

		#######################################################

                # add dans la closed list the father node
                # si on arrive sur la target alors reconstituer le chemin
                # end condition

                # test de merde :
                for i in open_list:
                        if (check_same_map(goal, i.map) == 1):
                                data = i
                                finish = 1
                                #exit(1)
				continue

                if (finish == 1):
                        continue
                else:
                        closed_list.append(data)
                        #sinon alors on continu notre algo
                        #open_list.sort(key=lambda Node : Node.f, reverse=False)

		######################## useless test
		#if (len(open_list) >= 100):
		#	for i in range(0, len(open_list)):
		#		print(open_list[i].f)
		#	print((open_list.pop()).f)
		#	exit(1)

	############################################################################

        answer = []
        while (data != None):
                try:
                        answer.append(data.map)
                        data = data.parent
                except:
                        print ("end bitch")
	print("Len path : " + str(len(answer)) + " | Closed list : " + str(len(closed_list)) + " | Open list : " + str(len(open_list)))

        return (answer)


def main():
	id_line = {}
	goal = [[1,2,3], [8,0,4], [7,6,5]]
	taquin = [[4,8,3], [5,7,2], [0,1,6]]#[[,,], [,,], [,,]]
	#taquin = [[1,2,3], [4,5,6], [7,0,8]]
	#taquin = [[1, 5, 2], [3, 5, 7], [6, 8, 0]]

	# 2moove
	#taquin = [[1,2,3], [4,0,5], [7,8,6]]
	path = astar(goal, taquin)
	path = path[::-1]
	print (path)

if __name__ == '__main__':
	start_time = time.time()
        main()
	print("--- %s seconds ---" % (time.time() - start_time))

