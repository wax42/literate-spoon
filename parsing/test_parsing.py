# basic parser 3 * 3 with py taquin generator

#!/usr/bin/python

import sys
import argparse

def usage_input(name):
	#print ("python [name] -f [file_name] -h [heuristique name] --graphics_mode --save [name_file]")
	print("python " + name + " -f [file] -h [hamming/other1/other2] --save [name_file] --graphic_mode --stats")

def parser_3_3():
	print(sys.argv)

	size = len(sys.argv)
	dim = int(sys.argv[6])

	if (dim != 3):
		print("*** ERROR DETECTED *** bad dim")
		exit(1)

	matrice = [[0] * dim for i in range(dim)]

	begin = 7
	act = 0
	try:
		for i in range(begin, size):
			matrice[act / 3][act % 3] = int(sys.argv[i])
			print (str(act / 3) + " : " + str(act % 3))
			act += 1
	except:
		print "*** ERROR DETECTED ***"
		exit(1)
	return (matrice)

# commentaire
# dimension
# data
def parser_v2(name_file):
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
			dim = int(line)
			sys.stdout.write("DIM : " + line)
			count += 1

	print ("Get dim " + str(dim))
	# get matrice of dim DIM
	matrice = [[0] * dim for i in range(dim)]
	for i in range(0, dim):
		line = f.readline()
		print(line)
		if (data[0] == "#" or data[0] == "\n"):
			print "COMMENT"
		else:
			data = line.split()
			print(data)
			for x in range(0, dim):
				matrice[i][x] = int(data[x])
		print (line)
	f.close()
	return matrice

def main():
	matrice = []
	if (len(sys.argv) < 2):
		usage_input(sys.argv[0])
		return (0)
	try:
		matrice = parser_v2(sys.argv[1])
	except:
		print ("Fucking error")
		return (0)
	print (matrice)
	return (matrice)

if __name__ == '__main__':
	main()
