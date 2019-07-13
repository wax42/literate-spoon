from algo_src.utils import random_puzzle, validate_random_puzzle, is_solvable
from algo_src.a_star import astar_launch, astar_setting

from algo_src.heuristique import check_gaschnig, check_hamming, check_manhattan

import pprint

def test_one_dim_all_heuristics(nb_test, dim, factor):
	dico_result = {}
	for i in range(nb_test):
		pzl = validate_random_puzzle(dim)
		result = []

		print("TEST GASHNIG")
		result.append(astar_launch(check_gaschnig, pzl, dim, factor))
		print("TEST MANHATTAN")
		result.append(astar_launch(check_manhattan, pzl, dim, factor))	

		print("TEST HAMMING")
		result.append(astar_launch(check_hamming, pzl, dim, factor))

		dico_result["TEST_N" + str(i)] = result
	return dico_result



def test_one_dim_factor(nb_test, dim, h, min_factor, max_factor):
	dico_result = {}
	stats = {}
	for i in range(nb_test):
		pzl = validate_random_puzzle(dim)
		dico_result["TEST_N" + str(i)] = []

		for j in range(min_factor, max_factor  + 1):
			print("TEST FACTOR ", j)
			result = astar_launch(h, pzl, dim, j)

			time_duration = result['time_duration']
			len_path = result['len_path']
			stats["FACTOR" + str(j)] = {
				"time_duration": time_duration,
				"len_path": len_path
			}
			dico_result["TEST_N" + str(i)].append(result)

		return dico_result, stats




def create_stats_heuristics(dico_result, nb_test):
	stats = {}
	for i in range(nb_test):
		gaschnig = dico_result["TEST_N" + str(i)][0]['time_duration']
		manhattan = dico_result["TEST_N" + str(i)][1]['time_duration']
		hamming = dico_result["TEST_N" + str(i)][2]['time_duration']
		new = {}
		if (gaschnig < manhattan and gaschnig < hamming):
			new['heuristics'] = 'gaschnig'
			new['time_duration'] = gaschnig

		elif (manhattan < gaschnig and manhattan < hamming):
			new['heuristics'] = 'manhattan'
			new['time_duration'] = manhattan

		elif (hamming < manhattan and hamming < gaschnig):
			new['heuristics'] = 'hamming'
			new['time_duration'] = hamming
		stats["TEST_N" + str(i)] = new
	return stats



def main(nb_test, dim_min, dim_max, factor):
	#  Check diffents heuritics and create stats with the faster factor
	list_result = {}
	stats = {}
	for i in range(dim_min, dim_max + 1):
		list_result[str(i)] = test_one_dim_all_heuristics(nb_test, i, factor)
		stats[str(i)] = create_stats_heuristics(list_result[str(i)], nb_test)
	
	pprint.pprint(list_result)
	print(" Heuristique la plus rapide")
	pprint.pprint(stats)


	
	# list_result = {}
	# stats = {}
	# #  Check diffents factors and create stats with the faster factor
	# for i in range(dim_min, dim_max + 1):
	# 	list_result[str(i)], stats[str(i)] = test_one_dim_factor(nb_test, i, check_manhattan, 0, 1)

	# print(" Go checher factor le plus intelligent")
	# #  Conclusion laisser le factor entre 0 et 1

	# pprint.pprint(stats)




if __name__ == '__main__':
	# To test A*
	nb_test = 1
	# min dim = 3 
	dim_min = 3
	# max dim = 3
	dim_max = 8
	factor = 1
	main(nb_test, dim_min, dim_max, factor)
	# To test greedy search
	factor = 0
	main(nb_test, dim_min, dim_max, factor)
