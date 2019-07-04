# !/usr/bin/python3
# coding: utf8

from .utils import puzzle_to_list
# RETROUVER LES POSITION DES CASES DU GOAL


def create_position_array(n):
	position_array = []
	for i in range(n):
		for j in range(n):
			pos = i,j
			position_array.append(pos)
	return position_array



def check_manhattan(taquin_map, goal):
	cost = 0
	size = len(taquin_map)
	taquin_map = puzzle_to_list(taquin_map)
	goal = puzzle_to_list(goal)
	#  rewrite in double array
	for i in range(size*size):
		if taquin_map[i] != 0 and taquin_map[i] != goal[i]:
			ci = goal.index(taquin_map[i])
			y = (i // size) - (ci // size)
			x = (i % size) - (ci % size)
			cost += abs(y) + abs(x)
	return (cost)



def check_gaschnig(taquin, goal):
    res = 0
    size = len(taquin) # TODO transfere la size a chaque fois en argument au lieu de recalculer
    taquin = puzzle_to_list(taquin) # TODO eviter de reconvertir en list a chaque fois
    goal = puzzle_to_list(goal)
    taquin = list(taquin)
    goal = list(goal)
    # On itere jusqu'a ce que notre taquin devienne le goal et on retourne le nombre d'iteration
    while taquin != goal:
        # On va chercher l'index du 0 dans notre taquin
        index = taquin.index(0)
        if goal[index] != 0:
            # Si goal[index] == 0 alors
            # On recupere le nombre situé dans goal a l index d avant
            # On recupere l'index de ce nombre la dans notre taquin
            ci = taquin.index(goal[index])
            # et on swap
            taquin[ci], taquin[index] = taquin[index], taquin[ci]
        else:
            # Si goal[index] != 0 alors on swap des qu'on trouve une difference
            for i in range(size * size):
                if goal[i] != taquin[i]:
                    taquin[i], taquin[index] = taquin[index], taquin[i]
                    break
        res += 1
    return res

        


# differene entre deux map, nb different case
# Hamming distance
def check_hamming(taquin_map, goal):
	nb_diff = 0
	for y in range(0, len(taquin_map)):
			for x in range(0, len(taquin_map[0])):
					if (taquin_map[y][x] != goal[y][x] and taquin_map[y][x] != 0):
							nb_diff += 1
	return (nb_diff)

