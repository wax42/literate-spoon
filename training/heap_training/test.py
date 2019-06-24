import heapq
import random

print ("coucou toi")

h = []

for i in range(0, 50):
	rand = random.randint(1, 1000)
	print ("push elem : " + str(rand))
	heapq.heappush(h, (rand, "coucou toi"))

print("=== BEGIN POP HEAPQ ===")

try:
	for i in range(0, 50):
		print(heapq.heappop(h))
except:
	print ("No enough item")
