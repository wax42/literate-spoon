import time
import argparse
from algo_src.my_argparse import parsing_bitch
from algo_src.heuristique import *
from algo_src.a_star import astar_launch

# file to launch alone the script without the web UI

def main(parse):
	print(argparse.__file__)

	parse = parsing_bitch() 
	print(parse.matrice)

	path = astar_launch(parse.heuristique, parse.matrice, parse.dim, parse.factor)
	path = path[::-1]
	return (str(path))

if __name__ == '__main__':
	parse = parsing_bitch()
	start_time = time.time()
	path = main(parse)
	print ("SECONDS       : %.3f" % (time.time() - start_time))
