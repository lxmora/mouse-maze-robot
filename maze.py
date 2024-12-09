import numpy as np

import webhandler as wh
from constants import *


class Node():

    def __init__(self):
        self.top = False
        self.left = False
        self.visit_state = 0 # 0 = unseen, 1 = seen, 2 = visited


class Maze():

    def __init__(self, max_depth : int, position : tuple, maze_array=None):
        self.server = wh.WebHandler()
        self.maze_buffer = self.server.get_maze()
        self.max_depth = max_depth
        self.current_position = list(position)
        self.view_size = 11
        self.center_offset = (5,5)
        self.symbol_size = 2
        if maze_array == None:
            self.maze_array = np.array([[Node() for _ in range(max_depth+1)] for _ in range(max_depth+1)])

    def update_maze(self):
        self.maze_buffer = self.server.get_maze()

    def move_left(self):
        self.server.request_movement('l')
        self.current_position[0] += -1

    def move_right(self):
        self.server.request_movement('r')
        self.current_position[0] += 1

    def move_up(self):
        self.server.request_movement('u')
        self.current_position[1] += 1

    def move_down(self):
        self.server.request_movement('d')
        self.current_position[1] += -1

    def process_maze_string(self, maze_string = None):
        if maze_string == None: maze_string = self.server.get_maze()

        top_edges=TOP_EDGE_VECS
        left_edges=LEFT_EDGE_VECS

        top_edges=self.check_edges(maze_string, top_edges)
        left_edges=self.check_edges(maze_string, left_edges)

        for edge in top_edges:
            vec = (edge[0],edge[1]+1)
            vec = self.to_global_vec(vec)
            node=self.maze_array[(vec)]
            node.top=True
            node.visit_state=1

        for edge in left_edges:
            vec = (edge[0]+1,edge[1])
            vec = self.to_global_vec(vec)
            node=self.maze_array[(vec)]
            node.left=True
            node.visit_state=1

    def check_edges(self, maze_string, edge_list):
        present_edges=[]
        for edge in edge_list:
            if maze_string[self.vec_to_index(edge)] == " ":
                present_edges.append(edge)
            elif maze_string[self.vec_to_index(edge)] == "█":
                pass
        return present_edges
    
    def vec_to_index(self, vec):
        return ((vec[0]*self.symbol_size)+(vec[1]*self.symbol_size*self.view_size))

    def to_global_vec(self, vec):
        current_x=self.current_position[0]
        current_y=self.current_position[1]
        vec_x=vec[0]
        vec_y=vec[1]
        offset_x=self.center_offset[0]
        offset_y=self.center_offset[1]

        global_x=current_x+((vec_x-offset_x)//2)
        global_y=current_y+((vec_y-offset_y)//2)
        return (global_x,global_y)
    

# --- Debug and Testing ---

test_string='20 text/gemini\n```A maze with a mouse in the middle\n██  ██████████  ██  ██\n██`,██🐁██🐁  `,  `,██\n██████  ██████  ██  ██\n██🐁  🐁  🐁██`,██🐁  \n██  ██  ██  ██████  ██\n  🐁██🐁██🐀  🐁██🐁██\n██  ██████  ██████  ██\n██🐁  🐁██🐁  🐁  🐁  \n██  ██████  ██  ██████\n  `,  `,██🐁██🐁  🐁██\n██  ██████████████████\n```\n\n=> /maze/app?l Left\n=> /maze/app?d Down\n=> /maze/app?u Up\n=> /maze/app?r Right\n\n## Etchings\n\n=> /maze/app/etch Etch something into the wall\n\nSome words are etched into the wall here.\n\n> Oh hey, I think I may have found a bug? I can\'t continue past this intersection if I come from above or below - I have to go right into the side corridor and then come back.\n>    - packbat, 2020-12-24\n\n> Heads-up from Packbat a bit later: figured it out. Laplace isn\'t following the link when it directs the browser to the exact same URL - to keep going in a direction, I have to reload the page instead.\n>    - packbat, 2020-12-24\n\n> *Lagrange. It\'s called Lagrange, not Laplace.\n>    - packbat, 2020-12-24\n\n> Sorry to leave such a mess right here on the beginning of the course - and hello, fellow maze-walkers! Hope y\'all have a worthwhile time poking around this space.\n>    - packbat, 2021-01-02\n\n> Packbat — I have noticed the same thing.  I hadn\'t tried the reload.  That might be not a bad way to handle it.  I just noticed the won\'t reload, if a link uses the same format.  That is a Lagrange issue maybe?\n>    - Jigme, 2021-01-31\n\n> As far as I can tell, "how should a client respond to the user clicking a circular link" is not covered by the spec - perhaps something like a special loopback symbol for such link would be appropriate? We might talk to the Lagrange developer about it if we work up the courage.\n>    - packbat, 2021-01-31\n\n> Update on Lagrange: the "no following a link to the current page" code was a workaround for a bug which the dev believes is patched, so it should be removed in future releases!\n>    - packbat, 2021-02-01\n\n> am mouse. brain small\n>    - jake87, 2021-02-07\n\n> There\'s a very LONG BRANCH if you go DOWN and LEFT. It\'s possible that the EXIT is there\n>    - Tau0, 2021-02-09\n\n> nice\n>    - misterv, 2021-02-10\n\n> Hello Everyone!\n>    - Volki57, 2021-02-16\n\n> Oh, that\'s fascinating - there\'s an algernon mouse on the leaderboard who is absurdly far away from the origin! I wonder if someone brought some code to bear on navigating the maze...\n>    - packbat, 2021-02-21\n\n> Belated final Lagrange update: the "load circular link" thing is indeed fixed. Hi to everyone else using this browser!\n>    - packbat, 2021-02-28\n\n> hola\n>    - daman, 2021-03-03\n\n> I walked a long way out into the maze, but now I\'ll wait here, for now. I think the value of the maze is in the messages others leave. \n>    - twotwos, 2021-05-17\n\n> @packbat\n> \n> Algernon\'s my mouse. I implemented a simple wall-following algorithm and set it loose. I assumed the maze was enclosed, except for the exit, and figured this would be the best way to find and record as many messages as possible.\n> \n> Code\'s here, if anyone\'s interested. It uses the diohsc browser.\n>  gemini://lyk.so/files/maze.sh\n>    - lykso, 2022-01-19\n\n> amf\n>    - taleq, 2024-08-23\n\n## Users\n\nYou spot these fellow rats also milling about here:\n* bb\n* jone\n* lykso\n* mattrim5989\n* olive\n* sam\n* shifty\n* taleq\n\n## Misc\n\n=> /maze/account Account Settings\n=> /maze/app/leaderboard Leaderboard\n=> /maze/https://gitlab.com/Alch_Emi/mice-in-space Source Code\n'

def build_marked_maze(maze, edge_list):
    maze=list(map("".join, zip(*[iter(maze)]*2)))
    for j in range(11):
        for i in range(11):
            if (i,j) in edge_list:
                print("XX",end='')
            else:
                print(maze[i+j*11],end='')
        print()

m=Maze(100, (-1,0))
m.move_right()
print(build_marked_maze(m.maze_buffer,[]))
