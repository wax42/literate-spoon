import argparse
import sys
from .heuristique import check_manhattan, check_hamming, check_gaschnig

class Parsing():
	def __init__(self):
		self.dim = 0
		self.matrice = 0
		self.factor = 0
		self.heuristique = 0
		self.error = 0

def parser_file(parse, name_file):
	f = open(name_file, "r")
	count = 0
	line = "coucou"
	dim = 0

	# get dim
	while line and count == 0:
			line = f.readline()
			data = line.split(' ')
			if (data[0] == "#" or data[0] == "\n"):
					sys.stdout.write("COMMENT : " + line)
			elif (count == 0):
					parse.dim = dim = int(line)
					sys.stdout.write("DIM : " + line)
					count += 1

	# get matrice of dim DIM
	matrice = [[0] * dim for i in range(dim)]
	for i in range(0, dim):
			line = f.readline()
			print(line, end="")
			if (data[0] == "#" or data[0] == "\n"):
					print("COMMENT")
			else:
					data = line.split()
					for x in range(0, dim):
							matrice[i][x] = int(data[x])
	f.close()
	parse.matrice = matrice
	return matrice

# find heurisisque function with string and affect function ptr
def parser_heuristique(parse, name_hr):
	name_hr = name_hr[0]
	print ("name heuristique" + name_hr)
	parse.heuristique = check_manhattan

	if (name_hr in "gaschnig"):
		print ("[+] gaschnig heuristique")
		parse.heuristique = check_gaschnig
	elif (name_hr in "hamming"):
		print ("[+] hamming heuristique")
		parse.heuristique = check_hamming
	elif (name_hr in "manhattan"):
		print ("[+] manhattan heuristique")
		parse.heuristique = check_manhattan

def main_arg():

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', nargs=1, help="input file", required=True)
	parser.add_argument('-e', '--heuristique', nargs=1, choices=['hamming', 'manhattan', 'gaschnig'], default=["hamming"], help='choose an heuristique')
	parser.add_argument('--factor', default = [0], type=int, nargs=1)

	# parse argument
	args = parser.parse_args()
	return (args)

#if __name__ == '__main__':
def main_parsing():
	try:
		parse = Parsing()
		args = main_arg()
		parser_file(parse, args.f[0])
		parser_heuristique(parse, args.heuristique)
		parse.factor = args.factor[0]
		return (parse)
	except:
		print("*** Error parsing argument")
		exit(0)
