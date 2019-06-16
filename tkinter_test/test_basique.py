from Tkinter import *

root = Tk()

# text
obj = Label(text="zone de text")
obj.config(text="bibitch", state=DISABLED) # griser la zone
obj.config(text="grosse pute", state=NORMAL)
obj.pack()

bouton = Button(text="john the button")
bouton.pack()

bt_img = Button()
#imm = PhotoImage(file="~/Images/aa.png")
#bt_img.config(image=imm)
bt_img.pack()

# zone de saisie
saisie = Entry()
saisie.insert(0, "content")
saisie.pack()

# combo box need ttk
#b = Combobox(root, values=["hamming", "h2", "h3"])
#b.pack()

# canva creation

w = 500
h = 500

w_case = 3
h_case = 3

w_incr = w / w_case
h_incr = h / h_case

pos = [0, 0]

graph = Canvas()

graph.config(width = w, height = h)

color  = "red"

def edit_canva_down():
	global graph
	pos[1] += 1
	#graph.create_rectangle(x * w_incr, y * h_incr, (x + 1) * w_incr, (y + 1) * h_incr, fill="red")
	graph.create_rectangle(pos[0] * w_incr, pos[1] * h_incr, (pos[0] + 1) * w_incr, (pos[1] + 1) * h_incr, fill=color)
	#pos[0] += 1
	print(pos)

def edit_canva_up():
        global graph
        pos[1] -= 1
        #graph.create_rectangle(x * w_incr, y * h_incr, (x + 1) * w_incr, (y + 1) * h_incr, fill="red")
        graph.create_rectangle(pos[0] * w_incr, pos[1] * h_incr, (pos[0] + 1) * w_incr, (pos[1] + 1) * h_incr, fill=color)
        #pos[0] += 1
        print(pos)

def edit_canva_left():
        global graph
        pos[0] += 1
        #graph.create_rectangle(x * w_incr, y * h_incr, (x + 1) * w_incr, (y + 1) * h_incr, fill="red")
        graph.create_rectangle(pos[0] * w_incr, pos[1] * h_incr, (pos[0] + 1) * w_incr, (pos[1] + 1) * h_incr, fill=color)
        #pos[0] += 1
        print(pos)

def edit_canva_right():
        global graph
        pos[0] -= 1
        #graph.create_rectangle(x * w_incr, y * h_incr, (x + 1) * w_incr, (y + 1) * h_incr, fill="red")
        graph.create_rectangle(pos[0] * w_incr, pos[1] * h_incr, (pos[0] + 1) * w_incr, (pos[1] + 1) * h_incr, fill=color)
        #pos[0] += 1
        print(pos)

def color_red():
	global color
	color = "red"

def color_green():
	global color
	color = "green"

#graph.create_rectangle(100,100,200,200, fill="blue", width=2)
for y in range(0, h_case):
	for x in range(0, w_case):
		data = "{x : " + str(x) + " | y : " + str(y) + "}"
		graph.create_rectangle(x * w_incr, y * h_incr, (x + 1) * w_incr, (y + 1) * h_incr, fill="blue")
		graph.create_text(x * w_incr + w_incr / 2, y * h_incr + h_incr / 2, text=data, fill="black", font=("arial", 18))

graph.pack()

b = Button(text="down", command=edit_canva_down)
b.pack()
b = Button(text="up", command=edit_canva_down)
b.pack()
b = Button(text="left", command=edit_canva_left)
b.pack()
b = Button(text="right", command=edit_canva_right)
b.pack()
b = Button(text="red",   command=color_red)
b.pack()
b = Button(text="green", command=color_green)

b.pack()

root.mainloop()
