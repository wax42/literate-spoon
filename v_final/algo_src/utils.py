import random


def map_str(map, dim):
	string = ""
	for y in range(0, dim):
		for x in range(0, dim):
			string += str(map[y][x])
	return (string)


# find element 0
def check_pos_empty(taquin_map):
	for y in range(0, len(taquin_map)):
		for x in range(0, len(taquin_map[0])):
			if (taquin_map[y][x] == 0):
				return (y, x)
	return (-1, -1)

def spiral(n):
	size = n * n

	dx,dy = 0,1	# Starting increments
	x,y = 0,0	# Starting location
	puzzle = [[None] * n for j in range(n)]
	for i in range(size):
		# x y  is good ?
		puzzle[x][y] = i + 1
		nx, ny = x + dx, y + dy
		if 0 <= nx < n and 0 <= ny < n and puzzle[nx][ny] == None:
			x, y = nx, ny
		else:
			dx, dy = dy,-dx
			x, y = x + dx, y + dy

	# Put 0 in the biggest elem
	for y in range(n):
		for x in range(n):
			if (puzzle[y][x] == size):
				puzzle[y][x] = 0
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

def is_solvable(puzzle, goal, dim):
        # PUZZLE VERIF SOLVABLE
        tab_map = []
        tab_goal = []
        for i in puzzle:
                tab_map = tab_map + i
        for i in goal:
                tab_goal = tab_goal + i

        v1 = find_n_simple_tab(tab_map)
        v2 = find_n_simple_tab(tab_goal)

        if (dim % 2 == 0):
                v1 += (find_pos_in_tab(tab_map, 0) / dim)
                v2 += (find_pos_in_tab(tab_goal, 0) / dim)
        if (v1 % 2 == v2 % 2):
                return (1)
        else:
                return (0)


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
	# Put 0 in the biggest elem
	size = n * n
	for y in range(n):
		for x in range(n):
			if (puzzle[y][x] == size):
				puzzle[y][x] = 0

	
	return puzzle

def find_pos_in_tab(tab, val):
        count = 0
        for i in tab:
                if (i == val):
                        return (count)
                count += 1
        return (count)

def find_n_simple_tab(map):
        size = len(map)
        n = 0
        for x in range(0, size):
                for xx in range(x+1, size):
                        if (map[x] > 0 and map[xx] > 0 and map[x] > map[xx]):
                                n = n + 1
        return (n)


def validate_random_puzzle(dim):
		goal = spiral(dim)
		solvable = 0
		while (solvable == 0):
			pzl = random_puzzle(dim)
			solvable = is_solvable(pzl, goal, dim)
		return pzl
