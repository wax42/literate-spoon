
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

	def set_map(self, map):
		self.map = map


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


	for y in range(0, len(puzzle)):
		for x in range(0, len(puzzle[0])):
			if (puzzle[y][x] == size):
				puzzle[y][x] = 0
	return puzzle
