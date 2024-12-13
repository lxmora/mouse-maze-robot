import pickle

import numpy as np

import webhandler as wh
from constants import EDGE_TILE_MAP, LEFT_EDGE_VECS, TOP_EDGE_VECS


class Node():

    def __init__(self):
        self.top = False
        self.left = False
        self.visit_state = 0 # 0 = unseen, 1 = seen, 2 = visited 3 = deadend
        self.wayback = ""

    def set_blocked(self):
        self.visit_state = 3



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
        if not fromload:
            if maze_array is None:
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
        print("saved maze data")

    def load(self=None):
        file=open("maze.dat","rb")
        savedata=pickle.load(file)
        print("loaded maze data")
        return Maze(savedata[0],savedata[1],savedata[2],fromload=True)

    def update_maze(self):
        self.maze_buffer = self.server.get_maze()

    def move_left(self):
        print("moving left")
        self.maze_buffer = self.server.request_movement('l')
        self.current_position[0] += -1

    def move_right(self):
        print("moving right")
        self.maze_buffer = self.server.request_movement('r')
        print("moving from",self.current_position,end="")
        self.current_position[0] += 1
        print("to",self.current_position)

    def move_up(self):
        print("moving up")
        self.maze_buffer = self.server.request_movement('u')
        self.current_position[1] += 1

    def move_down(self):
        print("moving down")
        self.maze_buffer = self.server.request_movement('d')
        self.current_position[1] += -1

    def check_adjacent(self):
        x_pos=self.current_position[0]
        y_pos=self.current_position[1]
        return {"left":self.get_node((x_pos,y_pos)).left,"up":self.get_node((x_pos,y_pos)).top,"right":self.get_node((x_pos+1,y_pos)).left,"down":self.get_node((x_pos,y_pos-1)).top}

    def process_maze_string(self):
        maze_string = self.maze_buffer

        top_edges=TOP_EDGE_VECS
        left_edges=LEFT_EDGE_VECS

        top_edges=self.check_edges(maze_string, top_edges)
        left_edges=self.check_edges(maze_string, left_edges)

        for edge in top_edges:
            vec = (edge[0],edge[1]+1)
            vec = self.to_global_vec(vec)
            self.set_top(vec)
            if self.get_node(vec).visit_state==0:
                self.set_state(vec, 1)

        for edge in left_edges:
            vec = (edge[0]+1,edge[1])
            vec = self.to_global_vec(vec)
            self.set_left(vec)
            if self.get_node(vec).visit_state==0:
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
        return self.maze_array[offest_vec]

    def get_current_node(self):
        vec=self.current_position
        return self.get_node(vec)
    
    def get_adjacent_nodes(self):
        vec=self.current_position
        adjacents={}
        adjacents["left"]=self.get_left_node()
        adjacents["right"]=self.get_right_node()
        adjacents["up"]=self.get_top_node()
        adjacents["down"]=self.get_bottom_node()
        return adjacents

    def get_left_node(self):
        vec=self.current_position
        vec[1]+= -1
        return self.get_node(vec)

    def get_right_node(self):
        vec=self.current_position
        vec[1]+= +1
        return self.get_node(vec)

    def get_top_node(self):
        vec=self.current_position
        vec[1]+= +1
        return self.get_node(vec)

    def get_bottom_node(self):
        vec=self.current_position
        vec[1]+= -1
        return self.get_node(vec)

    def set_state(self, node, state):
        node=self.get_node(node)
        node.visit_state=int(state)

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
