from algo_src.my_argparse import main_parsing
from algo_src.a_star import astar_launch

# file to launch alone the script without the web UI

# by example:
# python3 main.py -f sample_N-puzzle/dim_3 -e gaschnig

def main():
	parse = main_parsing() 
	if (astar_launch(parse.heuristique, parse.matrice, parse.dim, parse.factor) == -1):
		print("Error: path don't find")
		return (-1)
	return (0)

if __name__ == '__main__':
	main()
