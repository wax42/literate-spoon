# coding: utf8

from copy import deepcopy


# Afin de copier les states et de ne pas avoir d'erreur de "bindings"
# Se renseigner plus en détails
# https://docs.python.org/2/library/copy.html





# A heuristic function has the form:f^(n) = g^(n) + h^(n)

# where n represents some state, g^(n) is the lengthof the path to state n, 
# and h^(n) is the estimated distance of state n from the goal state. 
#  h^(n) is the heuristic part: this is usually an estimate.


# Gestion d'une Stack pourrait être intéressante afin de récupérer les states les plus petits le plus rapidement possible
# Surtout afin d'avoir ça en Objet proprement


# class Queue:
# 	"""
# 	https://docs.python.org/3.0/library/heapq.html

# 	Goal: Recode the basic function of heapq algorithm 

# 	or if it's possible use the librairy

# 	"""
# 	def heappop():
# 		"""
# 		Pop and return the smallest item from the heap, maintaining the heap invariant. If the heap is empty, IndexError is raised.
# 		"""
# 		pass

# 	def heappush():
# 		"""
# 		Push the value item onto the heap, maintaining the heap invariant.
# 		"""
# 		pass
	

# Possibility to declare the Goal, the k and the N Globally --> to have proper code

k = 3

N = k * k

puzzle = [ 
		6, 7, 8
		1, 2, 5,
		0, 3, 4 
]

goal = [
	1, 2, 3
	8, 0, 4
	7, 6, 5
]


class State:
	"""
	One State is defined by:

		g: the length of the path to state n
		path: all of the path to go in the state


	"""

	def __init__(self, puzzle, goal, k):
		# Possibility to declare the Goal, the k and the N Globally --> to have proper code

		self.puzzle = puzzle

		# Pour l'instant restons concentré sur des puzzles carrés. Par la suite, pour du bonus on s'amusera avec des rectangles


		# On va cherche où se situe la case vide
		for i in xrange(N):
			if (self.puzzle[i] == 0)
				self.pos0 = i
				break

		# Pour l'instant, on se concentre sur la distance de manhattan
		self.h = self.heuristic_manhattan()


	def heuristic_manhattan(self):
		"""  la distance de manhattan  
			 Mon ami Wiki https://fr.wikipedia.org/wiki/Distance_de_Manhattan

			For each tile, compute how many moves it would take to move that tile toits goal position 
			if there were no other tiles on the board. Add upthese distances for all of the tiles: 
			this gives a rough idea of how far this state is from the goal state



			Pourrait etre utile de renvoyer une lambda
			https://www.afternerd.com/blog/python-lambdas/

		"""
		# C'est très très brouillon

		# TODO mettre la formule au clair avant de taper du code 
		# return lambda x, y: x + self.movecount(y), xrange(N)
		for i in xrange(N):
			if (self.puzzle[i] == 0)
				break


	def movecount(self, i):
		""" 
			Trouver sur un forum perdu et qui m'a encore plus perdu
			TODO mettre la formule au clair avant de taper du code
		"""
        if self.puzzle[i] == 0:
            return 0
        return abs((i / k) - (self.puzzle[i] / k)) + abs((i % k) - (self.puzzle[i] % k))





	def heuristic_misplaced(self):
		""""
			Is to sumply count the number of tiles are not in their correct positions.

		"""
		pass

	def is_final(self):
		""" This function return True is the goal is good.

		In the subject, for an example of 3*3

		The goal is:
			1 2 3
			8 x 4
			7 6 5
		
		"""
		return self.goal == self.puzzle

	def move(self):
		"""
		This function return
			The New State 
			The indice of the Move 
		"""
		candidates = []
        # copy = deepcopy(self.puzzle)
		copy = self.puzzle
    
		
		# va falloir verifier tt ça 
	    if self.pos0 >= self.k:

            copy[self.pos0], copy[self.pos0 - self.k] = copy[self.pos0 - self.k], copy[self.pos0]
            candidates.append([State(copy), 'U'])
    
	    if self.pos0 < self.N - self.k:
            copy[self.pos0], copy[self.pos0 + self.k] = copy[self.pos0 + self.k], copy[self.pos0]
            candidates.append([State(copy), 'D'])
    
	    if (self.pos0 % self.k) > 0:
            copy[self.pos0], copy[self.pos0 - 1] = copy[self.pos0 - 1], copy[self.pos0]
            candidates.append([State(copy), 'L'])
    
	    if (self.pos0 % self.k) < self.k - 1:
            copy[self.pos0], copy[self.pos0 + 1] = copy[self.pos0 + 1], copy[self.pos0]
            candidates.append([State(copy), 'R'])
		return candidates




def check_is_valid_puzzle(puzzle):
	"""  
	To check is a valid or invalid puzzle look this shit:

	( en français pck c plus s1mple)

	http://villemin.gerard.free.fr/Puzzle/Taquin.htm

	
	"""
	pass



def astar(start):
	"""
	Wiki est mon ami

	https://fr.wikipedia.org/wiki/Algorithme_A*


	"""
	opened = [] # States to be examined and candidates to expansion

	# In opened we are going to put
	# g is the length of the state 
	# H is the results of the heuristic function 

	# [	g + H  , g , le state child, et le path  jusq'ici ]


	closed = [] # States already selected by the algorithm, compared to the solution, and expanded

	success = False

	# Queue.heappush(opened, [start.heuristic_manhattan(), 0, start, []])
	while (opened != [] and success == False):
		# cur =  = Queue.heappop(opened)
		if cur.is_final():  # compares cur to a solution state 
			return g, path
		else: 
			# remove cur to opened   --> interet de la queue avec heappop qui pop le state de la queue
			# add cur to closed
			closed.add(str(cur))  # A voir plus tard


			for child, move in cur.moves():
				# Go chercher les states de cur 


				if str(child) not in closed and str(child) not in opened:

					## LA FAUT METTRE LA FONCTION HEURISTTIC
					# On va commencer avec la distance de manhattan 



					p = path
					p.append(move)
					# Queue.heappush(opened, [g+1 + child.heuristic(), g+1, child, p])


	return None


def main():

	# Commençons par un exemple de 3*3


	moves = {'U':'UP', 'D':'DOWN', 'L':'LEFT', 'R':'RIGHT'}
	
	

	# g is the length of the state
	g, path = astar(State(puzzle))


if __name__ == '__main__':
	main()  