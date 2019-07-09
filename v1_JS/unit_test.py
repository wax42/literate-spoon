from algo_src.utils import random_puzzle, spiral
from algo_src.a_star import astar_launch, is_solvable, astar_setting

from algo_src.heuristique import check_gaschnig, check_hamming, check_manhattan

import pprint

def test_one_dim(nb_test, h, dim):
	list_result = []
	goal = spiral(dim)
	print("goal", goal)
	for i in range(nb_test):
		solvable = 0
		while (solvable == 0):
			pzl = random_puzzle(dim)
			solvable = is_solvable(pzl, goal, dim)
		print(solvable)
		print("test")
		# print(h, pzl, dim, 0)
		list_result.append(astar_launch(h, pzl, dim, 1))
	return list_result


def main(nb_test, dim_min, dim_max):
	list_result = {}
	for i in range(dim_min, dim_max):
		result = []
		print("TEST GASHNIG")
		result.append(test_one_dim(nb_test, check_gaschnig, i))	
		print("TEST MANHATTAN")

		result.append(test_one_dim(nb_test, check_manhattan, i))
		print("TEST HAMMING")

		result.append(test_one_dim(nb_test, check_hamming, i))

		list_result[str(i)] = result
	print("/n/n/n")
	pprint.pprint(list_result)

if __name__ == '__main__':
	# main(1, 3, 9)

	test_one_dim(1, check_gaschnig, 3)
	# dim = 3
	# goal = spiral(dim)
	# print(goal)
	# solvable = 0
	# while (solvable == 0):
	# 	pzl = random_puzzle(dim)
	# 	print(pzl)
	# 	solvable = is_solvable(pzl, goal, dim)
