import time
import argparse
from algo_src.my_argparse import main_parsing
# from algo_src.heuristique import *
from algo_src.a_star import astar_launch

# file to launch alone the script without the web UI

# by example:
# python3 main.py -f sample_N-po
# puzzle/dim_3 -e gaschnig

def main():
	print(argparse.__file__)

	parse = main_parsing() 
	path = astar_launch(parse.heuristique, parse.matrice, parse.dim, parse.factor)
	return (str(path))

if __name__ == '__main__':
	path = main()
