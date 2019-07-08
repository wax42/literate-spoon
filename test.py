#coding: utf8
import math
import pprint
import random

def count_conflicts(taquin_row, goal_row, size, ans=0):
	"""
	L'objectif de la fonction etant de compter le nombre de conflits

	"""
	# commençons par definir qu'est ce qu'un conflit

	# Two tiles tj and tk are in a linear conflict 
	# if tj and tk are the same line, the goal positions of 
	# tj and tk are both in that line, tj is to the right of tk,
	#  and goal position of tj is to the left of the goal position of tk.

	# disons tj == tile_1 and tk == til_2

	counts = [0 for x in range(size)]
	# Creation d'un tableau pour compter tout les conflits sur une ligne

	for i, tile_1 in enumerate(taquin_row):

            if tile_1 in goal_row and tile_1 != 0:
         
                    for j, tile_2 in enumerate(taquin_row):
         
                            if tile_2 in goal_row and tile_2 != 0:
         
                                    if tile_1 != tile_2:
                                            print(tile_1, "!=", tile_2)
                                            if (goal_row.index(tile_1) > goal_row.index(tile_2)) and i < j:
                                                    counts[i] += 1
                                            if (goal_row.index(tile_1) < goal_row.index(tile_2)) and i > j:
                                                    counts[i] += 1
                                    else:
                                        print(tile_1, "==", tile_2, "cad le batard est a la bonne place")
                            else:
                                print(tile_2, "n'est pas dans", goal_row)
            else:
                print(tile_1, "n'est pas dans", goal_row)

	if max(counts) == 0:
			# Si on a rien trouver retourner le resultat
	        return ans * 2
	else:
			# sinon ???
			i = counts.index(max(counts))
			taquin_row[i] = -1
			ans += 1
			return count_conflicts(taquin_row, goal_row, size, ans)


def gaschnig(taquin, goal, size):
    res = 0
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



def list_to_puzzle(lst):
    """
    Converts a one dimensional puzzle list and returns it's two dimensional representation.
    [1, 2, 3, 4, 5, 6, 7, 8, 0] --> [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    n_sqrt = int(math.sqrt(len(lst)))

    puzzle = []
    for i in range(0, len(lst), n_sqrt):
        line = []
        for j in range(0, n_sqrt):
            line.append(lst[i + j])
        puzzle.append(line)

    return puzzle


def puzzle_to_list(puzzle):
    """
    Converts a two dimensional puzzle to a one dimensional puzzle.
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]] --> [1, 2, 3, 4, 5, 6, 7, 8, 0]
    """
    lst = []
    for row in puzzle:
        lst.extend(row)
    return lst

def test_linearConlift():
	size = 3
	# for y in range(size):
	#         for x in range(size):
	#             idx = (y * size) + x
	#             print(idx)

	taquin_rows = [[] for y in range(size)] 
	taquin_columns = [[] for x in range(size)] 
	goal_rows = [[] for y in range(size)] 
	goal_columns = [[] for x in range(size)]

	taquin_map = [[7,5,0], [2 ,3 ,8], [4 ,6 ,1]]

	goal = [[1, 2, 3],[8 ,0 ,4],[7, 6 ,5]]

	goal_list = puzzle_to_list(goal)
	taquin_list = puzzle_to_list(taquin_map)

	res = 0

	for y in range(size):
		for x in range(size):

				idx = (y * size) + x
				
				# print("idx" ,idx)
				# print("xy", x, y)
				# print("Taquin result ", taquin_map[y][x])
				# print("Taquin list result ",taquin_list[idx])
				taquin_rows[y].append(taquin_map[y][x])
				taquin_columns[x].append(taquin_map[y][x])

				goal_rows[y].append(goal[y][x])
				goal_columns[x].append(goal[y][x])



	# print(taquin_rows)
	# print(taquin_columns)

	# print(goal_rows)
	# print(goal_columns)

	# Premiere etape OK
	# Let's go to check the fucking count_conflits function 

	pprint.pprint(taquin_rows)
	pprint.pprint(goal_rows)

	for i in range(size):
		# check lignes apres lignes dans l'exemple d'abord [7, 5, 0] avec [1, 2, 3] etc ...
		res += count_conflicts(taquin_rows[i], goal_rows[i], size)
	# for i in range(size):
	#         res += count_conflicts(taquin_columns[i], goal_columns[i], size)


def random_puzzle(n):
	size = n * n
	list_nb = [i + 1 for i in range(size)]

	puzzle = [[0] * n for _ in range(n)]
	for y in range(n):
		
		for x in range(n):
				random_nb = random.randint(0, size) - 1
				nb = list_nb[random_nb]
				list_nb.remove(nb)
				size = size - 1
				puzzle[y][x] = nb
	return puzzle



def main():
    print(random_puzzle(3))




if __name__ == "__main__":
	main()