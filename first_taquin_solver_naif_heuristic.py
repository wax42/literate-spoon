from copy import copy, deepcopy
import time

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

# differene entre deux map, nb different case
# Hamming distance
def check_hamming(taquin_map, goal):
	nb_diff = 0
	for y in range(0, len(taquin_map)):
		for x in range(0, len(taquin_map[0])):
			if (taquin_map[y][x] != goal[y][x] and taquin_map[y][x] != 0):
				nb_diff += 1
	return (nb_diff)

def check_manhattan(taquin_map, goal):
        cost = 0
	for y in range(0, len(taquin_map)):
		for x in range(0, len(taquin_map[0])):
                        if (taquin_map[y][x] == 0):
                                y_goal, x_goal = tableau_position[taquin_map[y][x]]
                                cost += abs(x_goal - x) - abs(y_goal - y)
	return (cost)

def check_LinearConflit(taquin_map, goal):
        
        
        def count_conflicts(taquin_row, goal_row, size, ans=0):
                counts = [0 for x in range(size)]
                for i, tile_1 in enumerate(taquin_row):
                        if tile_1 in goal_row and tile_1 != 0:
                                for j, tile_2 in enumerate(taquin_row):
                                        if tile_2 in goal_row and tile_2 != 0:
                                                if tile_1 != tile_2:
                                                        if (goal_row.index(tile_1) > goal_row.index(tile_2)) and i < j:
                                                                counts[i] += 1
                                                        if (goal_row.index(tile_1) < goal_row.index(tile_2)) and i > j:
                                                                counts[i] += 1
                if max(counts) == 0:
                        print("TEST GOOOD TEST ", ans)
                        return ans * 2
                else:
                        print("PRINT SALOPE DE TA MERE LA PUTE", ans)

                        i = counts.index(max(counts))
                        taquin_row[i] = -1
                        ans += 1
                        return count_conflicts(taquin_row, goal_row, size, ans)

        res = check_manhattan(taquin_map, goal)
        size = len(taquin_map)
        taquin_rows = [[] for y in range(size)] 
        taquin_columns = [[] for x in range(size)] 
        goal_rows = [[] for y in range(size)] 
        goal_columns = [[] for x in range(size)]

        # C PT CE QUE G FAIT LA 
        for y in range(size):
                for x in range(size):

                        taquin_rows[y].append(taquin_map[y][x])
                        taquin_columns[x].append(taquin_map[y][x])

                        goal_rows[y].append(goal[y][x])
                        goal_columns[x].append(goal[y][x])


        print(goal_columns)
        print(taquin_columns)

        # time.sleep(10)

        for i in range(size):
                res += count_conflicts(taquin_rows[i], goal_rows[i], size)
        for i in range(size):
                res += count_conflicts(taquin_columns[i], goal_columns[i], size)
        return res



FACTOR = 0

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
                                        newnode.h = check_LinearConflit(new_matrice, goal)
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


# Permet de retrouver la position des cases du GOAl

tableau_position = [
        (1, 1),
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (2, 1),
        (2, 0),
        (1, 0),
]

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
