# RETROUVER LES POSITION DES CASES DU GOAL
tableau_position = [
	(1, 1),
	(0, 0),
	(0, 1),
	(0, 2),
	(1, 2),
	(2, 2),
	(2, 1),
	(2, 0),
	(1, 0)
]

def puzzle_to_list(puzzle):
    """
    Converts a two dimensional puzzle to a one dimensional puzzle.
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]] --> [1, 2, 3, 4, 5, 6, 7, 8, 0]
    """
    lst = []
    for row in puzzle:
        lst.extend(row)
    return lst

def check_gaschnig(taquin, goal):
    res = 0
    size = len(taquin) # TODO transfere la size a chaque fois en argument au lieu de recalculer
    taquin = puzzle_to_list(taquin) # TODO eviter de reconvertir en list a chaque fois
    goal = puzzle_to_list(goal)
    taquin = list(taquin)
    goal = list(goal)
    # On itere jusqu'a ce que notre taquin devienne le goal et on retourne le nombre d'iteration
    while taquin != goal:
        # On va chercher l'index du 0 dans notre taquin
        index = taquin.index(0)
        if goal[index] != 0:
            # Si goal[index] == 0 alors
            # On recupere le nombre situé dans goal a l index d avant
            # On recupere l'index de ce nombre la dans notre taquin
            ci = taquin.index(goal[index])
            # et on swap
            taquin[ci], taquin[index] = taquin[index], taquin[ci]
        else:
            # Si goal[index] != 0 alors on swap des qu'on trouve une difference
            for i in range(size * size):
                if goal[i] != taquin[i]:
                    taquin[i], taquin[index] = taquin[index], taquin[i]
                    break
        res += 1
    return res




# differene entre deux map, nb different case
# Hamming distance
def check_hamming(taquin_map, goal):
        nb_diff = 0
        for y in range(0, len(taquin_map)):
                for x in range(0, len(taquin_map[0])):
                        if (taquin_map[y][x] != goal[y][x] and taquin_map[y][x] != 0):
                                nb_diff += 1
        return (nb_diff)

def check_manhattan(taquin_map, goal):
        cost = 0
        for y in range(0, len(taquin_map)):
                for x in range(0, len(taquin_map[0])):
                        if (taquin_map[y][x] == 0):
                                y_goal, x_goal = tableau_position[taquin_map[y][x]]
                                cost += abs(x_goal - x) - abs(y_goal - y)
        return (cost)


def check_linearConflit(taquin_map, goal):
        def count_conflicts(taquin_row, goal_row, size, ans=0):
                """
                L'objectif de la fonction etant de compter le nombre de conflits

                """
                counts = [0 for x in range(size)]
                for i, tile_1 in enumerate(taquin_row):
                        if tile_1 in goal_row and tile_1 != 0:
                                for j, tile_2 in enumerate(taquin_row):
                                        if tile_2 in goal_row and tile_2 != 0:
                                                if tile_1 != tile_2:
                                                        if (goal_row.index(tile_1) > goal_row.index(tile_2)) and i < j:
                                                                counts[i] += 1
                                                        if (goal_row.index(tile_1) < goal_row.index(tile_2)) and i > j:
                                                                counts[i] += 1
                if max(counts) == 0:
                        print("TEST GOOOD TEST ", ans)
                        return ans * 2
                else:
                        print("PRINT SALOPE DE TA MERE LA PUTE", ans)

                        i = counts.index(max(counts))
                        taquin_row[i] = -1
                        ans += 1
                        return count_conflicts(taquin_row, goal_row, size, ans)

        res = check_manhattan(taquin_map, goal)
        size = len(taquin_map)

        print("Size of taquin map", size)
        # creation de double tableau vide
        taquin_rows = [[] for y in range(size)] 
        taquin_columns = [[] for x in range(size)] 
        goal_rows = [[] for y in range(size)] 
        goal_columns = [[] for x in range(size)]
        

        # 
        for y in range(size):
                for x in range(size):

                        taquin_rows[y].append(taquin_map[y][x])
                        taquin_columns[x].append(taquin_map[y][x])

                        goal_rows[y].append(goal[y][x])
                        goal_columns[x].append(goal[y][x])


        print(goal_columns)
        print(taquin_columns)

        # time.sleep(10)

        for i in range(size):
                res += count_conflicts(taquin_rows[i], goal_rows[i], size)
        for i in range(size):
                res += count_conflicts(taquin_columns[i], goal_columns[i], size)
        return res

