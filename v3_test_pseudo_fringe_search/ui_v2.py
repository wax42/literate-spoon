
# from Tkinter import *
import tkinter as tk
import ast #for parsing

class Interface:
	def __init__(self, w, h, h_case=0, w_case=0):
		self.h = h
		self.w = w
		self.h_case = h_case
		self.w_case = w_case
		self.h_incr = 0
		self.w_incr = 0
		self.path = []
		self.len_path = 0
		self.root = tk.Tk()
		self.turn = 0 # actual turn
		self.graph = 0 # canva
		
		# canva creation
		self.graph = tk.Canvas()
		self.graph.config(width = self.w, height = self.h)


	def load_matrice(self, matrice_str, size_case=50):
		self.path = list(ast.literal_eval(matrice_str))
		self.len_path = len(self.path)
		self.h_case = self.w_case = len(self.path[0])
		# self.h_incr = self.h / self.h_case
		# self.w_incr = self.w / self.w_case
		self.h_incr = self.w_incr = size_case

def update_turn():
	global ui

	stringg = "Turn : " + str(ui.turn) + "/" + str(ui.len_path - 1)
	text_turn.config(text=stringg)

def update_screen():
	global ui

	for y in range(0, ui.h_case):
       		for x in range(0, ui.w_case):
                	data = str(ui.path[ui.turn][y][x])
                	ui.graph.create_rectangle(x * ui.w_incr, y * ui.h_incr, (x + 1) * ui.w_incr, (y + 1) * ui.h_incr, fill="blue")
                	ui.graph.create_text(x * ui.w_incr + ui.w_incr / 2, y * ui.h_incr + ui.h_incr / 2, text=data, fill="black", font=("arial", 18))
	

	x_start = ui.h / 2
	size_x = x_start / 2
	y_start = 0
	size_y = 3
	for i in range(0, ui.len_path):
		if (i == ui.turn):
			ui.graph.create_rectangle(x_start, y_start + i * size_y, x_start + size_x, y_start + (i + 1) * size_y, fill="red")
		else:
			ui.graph.create_rectangle(x_start, y_start + i * size_y, x_start + size_x, y_start + (i + 1) * size_y, fill="blue")
		



def incr_turn():
	global ui

	ui.turn = (ui.turn + 1)
	if (ui.turn >= ui.len_path):
		ui.turn = ui.len_path - 1
	update_screen()
	update_turn()

def decr_turn():
	global ui

	ui.turn -= 1
	if (ui.turn < 0):
		ui.turn = 0
	update_screen()
	update_turn()

def last_turn():
	global ui
	
	ui.turn = ui.len_path - 1
	update_screen()
	update_turn()

def first_turn():
	global ui

	ui.turn = 0
	update_screen()
	update_turn()

def add_boutton():
        tk.Button(text="incr", width=20, height=20, command=incr_turn).pack()
        tk.Button(text="decr", command=decr_turn).pack()
        tk.Button(text="begin turn", command=first_turn).pack()
        tk.Button(text="last turn", command=last_turn).pack()


def graphic_mode(string = 0):
	global ui
	global text_turn

	ui = Interface(500, 500)

	#matrice = "[[[7, 5, 0], [2, 3, 8], [4, 6, 1]], [[7, 0, 5], [2, 3, 8], [4, 6, 1]], [[7, 3, 5], [2, 0, 8], [4, 6, 1]], [[7, 3, 5], [2, 8, 0], [4, 6, 1]], [[7, 3, 0], [2, 8, 5], [4, 6, 1]], [[7, 0, 3], [2, 8, 5], [4, 6, 1]], [[0, 7, 3], [2, 8, 5], [4, 6, 1]], [[2, 7, 3], [0, 8, 5], [4, 6, 1]], [[2, 7, 3], [8, 0, 5], [4, 6, 1]], [[2, 7, 3], [8, 6, 5], [4, 0, 1]], [[2, 7, 3], [8, 6, 5], [4, 1, 0]], [[2, 7, 3], [8, 6, 0], [4, 1, 5]], [[2, 7, 3], [8, 0, 6], [4, 1, 5]], [[2, 0, 3], [8, 7, 6], [4, 1, 5]], [[0, 2, 3], [8, 7, 6], [4, 1, 5]], [[8, 2, 3], [0, 7, 6], [4, 1, 5]], [[8, 2, 3], [7, 0, 6], [4, 1, 5]], [[8, 2, 3], [7, 1, 6], [4, 0, 5]], [[8, 2, 3], [7, 1, 6], [0, 4, 5]], [[8, 2, 3], [0, 1, 6], [7, 4, 5]], [[8, 2, 3], [1, 0, 6], [7, 4, 5]], [[8, 2, 3], [1, 4, 6], [7, 0, 5]], [[8, 2, 3], [1, 4, 6], [7, 5, 0]], [[8, 2, 3], [1, 4, 0], [7, 5, 6]], [[8, 2, 3], [1, 0, 4], [7, 5, 6]], [[8, 2, 3], [1, 5, 4], [7, 0, 6]], [[8, 2, 3], [1, 5, 4], [0, 7, 6]], [[8, 2, 3], [0, 5, 4], [1, 7, 6]], [[8, 2, 3], [5, 0, 4], [1, 7, 6]], [[8, 2, 3], [5, 7, 4], [1, 0, 6]], [[8, 2, 3], [5, 7, 4], [0, 1, 6]], [[8, 2, 3], [0, 7, 4], [5, 1, 6]], [[8, 2, 3], [7, 0, 4], [5, 1, 6]], [[8, 2, 3], [7, 1, 4], [5, 0, 6]], [[8, 2, 3], [7, 1, 4], [5, 6, 0]], [[8, 2, 3], [7, 1, 0], [5, 6, 4]], [[8, 2, 3], [7, 0, 1], [5, 6, 4]], [[8, 2, 3], [7, 6, 1], [5, 0, 4]], [[8, 2, 3], [7, 6, 1], [0, 5, 4]], [[8, 2, 3], [0, 6, 1], [7, 5, 4]], [[8, 2, 3], [6, 0, 1], [7, 5, 4]], [[8, 2, 3], [6, 1, 0], [7, 5, 4]], [[8, 2, 3], [6, 1, 4], [7, 5, 0]], [[8, 2, 3], [6, 1, 4], [7, 0, 5]], [[8, 2, 3], [6, 1, 4], [0, 7, 5]], [[8, 2, 3], [0, 1, 4], [6, 7, 5]], [[8, 2, 3], [1, 0, 4], [6, 7, 5]], [[8, 0, 3], [1, 2, 4], [6, 7, 5]], [[0, 8, 3], [1, 2, 4], [6, 7, 5]], [[1, 8, 3], [0, 2, 4], [6, 7, 5]], [[1, 8, 3], [6, 2, 4], [0, 7, 5]], [[1, 8, 3], [6, 2, 4], [7, 0, 5]], [[1, 8, 3], [6, 0, 4], [7, 2, 5]], [[1, 0, 3], [6, 8, 4], [7, 2, 5]], [[0, 1, 3], [6, 8, 4], [7, 2, 5]], [[6, 1, 3], [0, 8, 4], [7, 2, 5]], [[6, 1, 3], [8, 0, 4], [7, 2, 5]], [[6, 1, 3], [8, 2, 4], [7, 0, 5]], [[6, 1, 3], [8, 2, 4], [0, 7, 5]], [[6, 1, 3], [0, 2, 4], [8, 7, 5]], [[0, 1, 3], [6, 2, 4], [8, 7, 5]], [[1, 0, 3], [6, 2, 4], [8, 7, 5]], [[1, 2, 3], [6, 0, 4], [8, 7, 5]], [[1, 2, 3], [0, 6, 4], [8, 7, 5]], [[1, 2, 3], [8, 6, 4], [0, 7, 5]], [[1, 2, 3], [8, 6, 4], [7, 0, 5]], [[1, 2, 3], [8, 0, 4], [7, 6, 5]]]"
	ui.load_matrice(string)

	text_turn = tk.Label(text="Turn x on x\n")
	text_turn.pack()

	turn = 0
	update_screen()
	ui.graph.pack()

	add_boutton()
	ui.root.mainloop()



#if __name__ == "__main__":
#	main()
