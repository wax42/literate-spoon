neigh = [[0, -1], [0, 1], [-1, 0], [1, 0]]

def calcul_pos_xy_1d(pos, dim):
	return ([pos % 3, pos / dim])

def calcul_pos_xy_2d(pts, dim):
	print("fuck : " + str(pts))
	return (pts[0] + pts[1] * dim)

# test de wap a une dimension
tab = [[1, 2, 3],[4, 5, 6],[7, 8, 9]]

tab1 = []

print (tab)

for i in tab:
	tab1 += i

#for i in range(0, 9):
#	#print(str(calcul_pos(i, 3)) + ") " + str(calcul_pos(i)))
#	print (calcul_pos_xy_1d(i, 3))
#	print (calcul_pos_xy_2d(calcul_pos_xy_1d(i, 3), 3))
#print (tab1)


pts = calcul_pos_xy_1d(5, 3)
print (pts)

print ("Generate adjacent pts : ")

for i in neigh:
	tmp_pts = [pts[0] + i[0], pts[1] + i[1]] 
	print (str(tmp_pts) + "---> " + str(calcul_pos_xy_2d(tmp_pts, 3)))
