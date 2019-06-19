import Queue

print "test Queue"

q = Queue.PriorityQueue(0)

q.put((3, "c"))
q.put((1, "a"))
q.put((2, "b"))

q.put((3, "dd"))
q.put((1, "aa"))
q.put((2, "bb"))

while q.qsize():
	a = q.get()
	print a[0]
	print a[1]
