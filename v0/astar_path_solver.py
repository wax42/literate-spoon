from Tkinter import *
import time

def quitter():
        racine.quit()

racine = Tk()
racine.protocol("WM_DELETE_WINDOW", quitter)
racine.geometry("+200+250")

Width = 800
Height = 800

cadre = Frame(racine, background="grey", width=Width, height=Height)
cadre.pack()

canva = Canvas(cadre, width=Width, height=Height, background="blue")
canva.grid(row=0, column=0)


class Node():
        def __init__(self, parent=None, pos=None):
                # case precedente
                self.parent = parent
                # pos de notre neud
                self.pos = pos

                # distance depuis le depart
                self.g = 0
                # heirstique
                self.h = 0

                # g + h
                self.f = 0

        def __eq__(self, other):
                return (self.pos == other.pos)

        def __str__(self):
                return ("pos : " + str(self.pos) + " | g : " + str(self.g) + " | h : " + str(self.h) + " | f : " + str(self.f))


def str_list_node(listNode):
        for i in listNode:
                print(listNode)

def euristique(pts1, pts2):
        return abs(pts1[0] - pts2[0]) + abs(pts1[1] - pts2[1])

# checker si une pos est dans la closed list
def check_pos_is_present(pts, closed_list):
        for i in closed_list:
                if pts[0] == i.pos[0] and pts[1] == i.pos[1]:
                        return 1
        return 0

FACTOR = 8

def astar(begin, end, maze):
        print ("fucking test")

        # tableau de 4 element qui 

        # initialisation des data
        start_node = Node(None, begin)
        end_node = Node(None, end)
        # permet e checker les voisiin par simple addition de pos via une boucle
        neightbours = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # initialisation des liste de priorite
        # noeud a analiser
        open_list = []
        # neud deja analize
        closed_list = []

        # tmp list
        #tmp_list = []

        # test de parcours de tout les elements:
        #for y in range(0, len(maze)):
        #       for x in range(0, len(maze[0])):
        #               print (str(y) + ":" + str(x) + ":" + str(maze[y][x]))

        # ici on store le premier noeud qui a un cout dez zero
        open_list.append(start_node)

        # algo:
        # pop open list
        # gen neightbours withtout in closedlist
        # add g, h, f
        finish = 0
        while len(open_list) and finish is 0:
                data = open_list.pop()
                print (" : open list len : " + str(len(open_list)) + " | closed list : " + str(len(closed_list)))
                # liste temporaire pour stoquer les chemins
                for i in neightbours:
                        pos_y = data.pos[0] + i[0]
                        pos_x = data.pos[1] + i[1]
                        # checker si notre noeud actuel n est pas dans la closed list
                        if check_pos_is_present((pos_y, pos_x), closed_list) == 0:
                                # checker si on est encore dans le range
                                if pos_x >= 0 and pos_y >= 0 and pos_x < len(maze[0]) and pos_y < len(maze):
                                        if maze[pos_y][pos_x] == 0:
                                                print("----> y : " + str(pos_y) + " | x : " + str(pos_x))
                                                newnode = Node(data, (data.pos[0] + i[0], data.pos[1] + i[1]))
                                                # calculer le g h and f
                                                newnode.g = data.g + 10
                                                newnode.h = euristique(newnode.pos, end)
                                                newnode.f = newnode.g + newnode.h
                                                open_list.append(newnode)

                # add dans la closed list the father node
                # si on arrive sur la target alors reconstituer le chemin
                # end condition

                # test de merde :
                for i in open_list:
                        #print "turn : " + str(i) + " | x : " + str(i.pos[1]) + " | y : " + str(i.pos[0]) + " | " + str(end[1]) + " | " + str(end[0])
                        if (i.pos[0] is end[0] and i.pos[1] is end[1]):
                                print ("find" + str(i))
                                data = i
                                finish = 1
                                continue

                if (finish == 1):
                        continue
                else:
                        closed_list.append(data)
                        #sinon alors on continu notre algo
                        open_list.sort(key=lambda Node : Node.f, reverse=True)
        print("KOUKOU : x : " + str(data.pos[0]) + " | y : " + str(data.pos[1]))
        answer = []
        while (data != None):
                try:
                        answer.append(data.pos)
                        data = data.parent
                except:
                        print ("end bitch")
        return (answer)

def main():
        id_line = {}
        maze = [[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
                [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
                [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                [0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
                [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]]

        start = (0, 0)
        end = (8, 0)

        path = astar(start, end, maze)
        path = path[::-1]
        print (path)

        max_x = len(maze[0])
        max_y = len(maze)
        incr_x = Width / max_x
        incr_y = Height / max_y

        for y in range(0, max_y):
                for x in range(0, max_x):
                        if (maze[y][x] == 0):
                                Color = "white"
                        else:
                                Color = "black"
                        id_line[y*max_x+x] = canva.create_rectangle(incr_y*y, incr_x*x, incr_y * (y+1), incr_x * (x+1), fill=Color)

        for yhea in path:
                Color = "Blue"
                canva.create_rectangle(incr_y*yhea[0], incr_x * yhea[1], incr_y * (yhea[0]+1), incr_x*(yhea[1]+1), fill=Color)
        #       time.sleep(2.0)
        racine.mainloop()

if __name__ == '__main__':
        main()




