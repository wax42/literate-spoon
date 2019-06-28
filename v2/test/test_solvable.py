# =======================================
# SOLVABLE FUNCTION
# use dim - 1 udpate nb_diff
# we need a factor of dim - 1
# else
# not solvable

# gen dictionnaries ascendancxe
def made_dict_asc(goal_map):
	dico_asc = dict()
	for i in range(0, len(goal_map)):
		dico_asc[goal_map[i]] = i
	return (dico_asc)

def get_nb_diff(start, dico_asc):
        nb_diff = 0
        size = len(start)
        for i in range(0, size):
                for x in range(i + 1, size):
                        if (start[i] > start[x]):
                                nb_diff += 1
        return (nb_diff)

###############################################3
#################################################

def check_solvable(dim, nb_diff):
        if (nb_diff % (dim - 1)):
                return (1)
        return (0)

print("--=== TEST ===--")

goal = [[1, 2, 3], [8 ,0 ,4], [7, 6 ,5]]

start = [0, 3, 8, 6, 5, 1, 7, 4,2]
start = [7, 5, 0, 2, 3, 8, 4, 6, 1]
goal_map = []

for i in goal:
	goal_map += i

print (goal)
print (goal_map)

dico_id = made_dict_asc(goal_map)

print ("dico id : ", end='')
print (dico_id)
print ("start : ", end='')
print (start)

print ("============================================")

nb_diff = get_nb_diff(start, dico_id)
is_solve = check_solvable(3, nb_diff)

print ("nb diff : " + str(nb_diff))


if (is_solve):
	print ("Solvable bitch :)")
else:
	print ("not solvable ....")
