# basic parser 3 * 3 with py taquin generator

#!/usr/bin/python

import sys

def parser_3_3():
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
			print i
			act += 1
	except:
		print "*** ERROR DETECTED ***"
		exit(1)
	return (matrice)

print (parser_3_3())
