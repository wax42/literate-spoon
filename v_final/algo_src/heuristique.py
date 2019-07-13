# !/usr/bin/python3
# coding: utf8
from .utils import puzzle_to_list

def check_manhattan(taquin_map, goal):
	cost = 0
	size = len(taquin_map)
	taquin_map = puzzle_to_list(taquin_map)
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
    size = len(taquin)
    taquin = puzzle_to_list(taquin)
    taquin = list(taquin)
    goal = list(goal)
    while taquin != goal:
        index = taquin.index(0)
        if goal[index] != 0:
            ci = taquin.index(goal[index])
            taquin[ci], taquin[index] = taquin[index], taquin[ci]
        else:
            for i in range(size * size):
                if goal[i] != taquin[i]:
                    taquin[i], taquin[index] = taquin[index], taquin[i]
                    break
        res += 1
    return res


def check_hamming(taquin_map, goal):
	taquin_map1d = puzzle_to_list(taquin_map)
	nb_diff = 0
	for x in range(0, len(taquin_map1d)):
		if (taquin_map1d[x] != goal[x] and taquin_map1d[x] != 0):
			nb_diff += 1
	return (nb_diff)