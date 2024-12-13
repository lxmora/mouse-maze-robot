import numpy as np
import pickle
import os

import webhandler as wh
from constants import *


class Node():

    def __init__(self):
        self.top = False
        self.left = False
        self.visit_state = 0 # 0 = unseen, 1 = seen, 2 = visited
        self.wayback = ""


class Maze():

    def __init__(self, max_depth : int, position : tuple, maze_array : np.ndarray = None, fromload=False):
        self.server = wh.WebHandler()
        self.maze_buffer = []
        self.update_maze()
        self.max_depth = max_depth
        self.current_position = list(position)
        self.view_size = 11
        self.center_offset = (5,5)
        self.symbol_size = 2
        if fromload == False:
            if maze_array == None:
                self.maze_array = np.array([[Node() for _ in range(max_depth+1)] for _ in range(max_depth+1)])
            else:
                self.maze_array = maze_array
        else:
            self.maze_array = maze_array

    def save(self):
        savedata=pickle.dumps([self.max_depth,self.current_position,self.maze_array])
        file=open("maze.dat","wb")
        file.write(savedata)
        file.close()

    def load():
        file=open("maze.dat","rb")
        savedata=pickle.load(file)
        print(savedata)
        return Maze(savedata[0],savedata[1],savedata[2],fromload=True)

    def update_maze(self):
        self.maze_buffer = self.server.get_maze()

    def move_left(self):
        self.maze_buffer = self.server.request_movement('l')
        self.current_position[0] += -1

    def move_right(self):
        self.maze_buffer = self.server.request_movement('r')
        self.current_position[0] += 1

    def move_up(self):
        self.maze_buffer = self.server.request_movement('u')
        self.current_position[1] += 1

    def move_down(self):
        self.maze_buffer = self.server.request_movement('d')
        self.current_position[1] += -1

    def check_left(self):
        curr_pos = self.current_position
        self.maze.get_node(tuple(curr_pos)).left

    def check_right(self):
        curr_pos = self.current_position
        curr_pos[0] += -1
        self.maze.get_node(tuple(curr_pos)).left
    
    def check_up(self):
        curr_pos = self.current_position
        self.maze.get_node(tuple(curr_pos)).top
    
    def check_down(self):
        curr_pos = self.current_position
        curr_pos[0] += -1
        self.maze.get_node(tuple(curr_pos)).top

    def process_maze_string(self):
        maze_string = self.maze_buffer

        top_edges=TOP_EDGE_VECS
        left_edges=LEFT_EDGE_VECS

        top_edges=self.check_edges(maze_string, top_edges)
        left_edges=self.check_edges(maze_string, left_edges)

        self.debug_edges=top_edges+left_edges

        for edge in top_edges:
            vec = (edge[0],edge[1]+1)
            print("Vec in:", vec, end=" ")
            vec = self.to_global_vec(vec)
            print("Top Edge Found :", edge, " --> Corresponding Vec:", vec)
            self.set_top(vec)
            self.set_state(vec, 1)

        for edge in left_edges:
            vec = (edge[0]+1,edge[1])
            vec = self.to_global_vec(vec)
            print("Left Edge Found :", edge, " --> Corresponding Vec:", vec)
            self.set_left(vec)
            self.set_state(vec, 1)

    def check_edges(self, maze_string : str, edge_list : list):
        present_edges=[]
        for edge in edge_list:
            if maze_string[self.vec_to_index(edge)] == " ":
                present_edges.append(edge)
            elif maze_string[self.vec_to_index(edge)] == "█":
                pass
        return present_edges

    def get_node(self, vec : tuple):
        offset=self.max_depth//2+1
        offest_vec = (vec[0]+offset,vec[1]+offset)
        print("converting", vec, "-->", offest_vec)
        return self.maze_array[offest_vec]

    def get_current_node(self):
        vec=self.current_position
        get_node(vec)

    def get_left_node(self):
        vec=self.current_position
        vec[1]+= -1
        get_node(vec)
    
    def get_right_node(self):
        vec=self.current_position
        vec[1]+= +1
        get_node(vec)

    def get_top_node(self):
        vec=self.current_position
        vec[1]+= +1
        get_node(vec)

    def get_bottom_node(self):
        vec=self.current_position
        vec[1]+= -1
        get_node(vec)

    def set_state(self, node, state):
        node=self.get_node(node)
        node.visit_state=state

    def set_left(self, node):
        node=self.get_node(node)
        node.left=True

    def set_top(self, node):
        node=self.get_node(node)
        node.top=True
    
    def vec_to_index(self, vec : tuple):
        return (((vec[0]*self.symbol_size))+((vec[1]*self.symbol_size*self.view_size)))

    def to_global_vec(self, vec : tuple):
        new_vec = EDGE_TILE_MAP[vec]
        curr_pos = self.current_position
        return (curr_pos[0]+new_vec[0],curr_pos[1]+new_vec[1])


# --- Debug and Testing ---

# test_string='20 text/gemini\n```A maze with a mouse in the middle\n██  ██████████  ██  ██\n██`,██🐁██🐁  `,  `,██\n██████  ██████  ██  ██\n██🐁  🐁  🐁██`,██🐁  \n██  ██  ██  ██████  ██\n  🐁██🐁██🐀  🐁██🐁██\n██  ██████  ██████  ██\n██🐁  🐁██🐁  🐁  🐁  \n██  ██████  ██  ██████\n  `,  `,██🐁██🐁  🐁██\n██  ██████████████████\n```\n\n=> /maze/app?l Left\n=> /maze/app?d Down\n=> /maze/app?u Up\n=> /maze/app?r Right\n\n## Etchings\n\n=> /maze/app/etch Etch something into the wall\n\nSome words are etched into the wall here.\n\n> Oh hey, I think I may have found a bug? I can\'t continue past this intersection if I come from above or below - I have to go right into the side corridor and then come back.\n>    - packbat, 2020-12-24\n\n> Heads-up from Packbat a bit later: figured it out. Laplace isn\'t following the link when it directs the browser to the exact same URL - to keep going in a direction, I have to reload the page instead.\n>    - packbat, 2020-12-24\n\n> *Lagrange. It\'s called Lagrange, not Laplace.\n>    - packbat, 2020-12-24\n\n> Sorry to leave such a mess right here on the beginning of the course - and hello, fellow maze-walkers! Hope y\'all have a worthwhile time poking around this space.\n>    - packbat, 2021-01-02\n\n> Packbat — I have noticed the same thing.  I hadn\'t tried the reload.  That might be not a bad way to handle it.  I just noticed the won\'t reload, if a link uses the same format.  That is a Lagrange issue maybe?\n>    - Jigme, 2021-01-31\n\n> As far as I can tell, "how should a client respond to the user clicking a circular link" is not covered by the spec - perhaps something like a special loopback symbol for such link would be appropriate? We might talk to the Lagrange developer about it if we work up the courage.\n>    - packbat, 2021-01-31\n\n> Update on Lagrange: the "no following a link to the current page" code was a workaround for a bug which the dev believes is patched, so it should be removed in future releases!\n>    - packbat, 2021-02-01\n\n> am mouse. brain small\n>    - jake87, 2021-02-07\n\n> There\'s a very LONG BRANCH if you go DOWN and LEFT. It\'s possible that the EXIT is there\n>    - Tau0, 2021-02-09\n\n> nice\n>    - misterv, 2021-02-10\n\n> Hello Everyone!\n>    - Volki57, 2021-02-16\n\n> Oh, that\'s fascinating - there\'s an algernon mouse on the leaderboard who is absurdly far away from the origin! I wonder if someone brought some code to bear on navigating the maze...\n>    - packbat, 2021-02-21\n\n> Belated final Lagrange update: the "load circular link" thing is indeed fixed. Hi to everyone else using this browser!\n>    - packbat, 2021-02-28\n\n> hola\n>    - daman, 2021-03-03\n\n> I walked a long way out into the maze, but now I\'ll wait here, for now. I think the value of the maze is in the messages others leave. \n>    - twotwos, 2021-05-17\n\n> @packbat\n> \n> Algernon\'s my mouse. I implemented a simple wall-following algorithm and set it loose. I assumed the maze was enclosed, except for the exit, and figured this would be the best way to find and record as many messages as possible.\n> \n> Code\'s here, if anyone\'s interested. It uses the diohsc browser.\n>  gemini://lyk.so/files/maze.sh\n>    - lykso, 2022-01-19\n\n> amf\n>    - taleq, 2024-08-23\n\n## Users\n\nYou spot these fellow rats also milling about here:\n* bb\n* jone\n* lykso\n* mattrim5989\n* olive\n* sam\n* shifty\n* taleq\n\n## Misc\n\n=> /maze/account Account Settings\n=> /maze/app/leaderboard Leaderboard\n=> /maze/https://gitlab.com/Alch_Emi/mice-in-space Source Code\n'
'''
def build_marked_maze(maze : Maze, edge_list : list):
    maze=list(map("".join, zip(*[iter(maze)]*2)))
    for j in range(11):
        for i in range(11):
            if (i,j) in edge_list:
                print("XX",end='')
            else:
                print(maze[i+j*11],end='')
        print()

os.nice(19)
#m=Maze.load()
m=Maze(5000, (0,0))

print(len(m.maze_array)/2)

while True:
    m.process_maze_string()
    build_marked_maze(m.maze_buffer,m.debug_edges)
    print()
    build_marked_maze(m.maze_buffer,[])
    x_pos=m.current_position[0]
    y_pos=m.current_position[1]
    print(m.current_position,"Left:",m.get_node((x_pos,y_pos)).left,", Top:",m.get_node((x_pos,y_pos)).top,", Right:",m.get_node((x_pos+1,y_pos)).left,", Down:",m.get_node((x_pos,y_pos-1)).top)
    for x in range(-2,3):
        for y in range(2,-3):
            print("("+str(x)+":"+str(y)+")"+".Left =",m.get_node((x,y)).left)
    i = input()
    if i == 'l':
        m.move_left()
    if i == 'r':
        m.move_right()
    if i == 'u':
        m.move_up()
    if i == 'd':
        m.move_down()
    if i == 's':
        m.save()
'''