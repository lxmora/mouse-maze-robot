import os
import time

import compass

from maze import Maze, Node

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

try:
    open("maze.dat",'r')
except:
    m=Maze(, (0,0))
else:
    m=Maze.load()
n=compass.Navigator(m)

mode=1

timer=time.time()
if __name__ == "__main__":
    while mode == 1:
        cycle_start=time.time()
        x_pos=m.current_position[0]
        y_pos=m.current_position[1]
        print(m.current_position,"Left:",m.get_node((x_pos,y_pos)).left,", Top:",m.get_node((x_pos,y_pos)).top,", Right:",m.get_node((x_pos+1,y_pos)).left,", Down:",m.get_node((x_pos,y_pos-1)).top,end=" ")
        n.wallfollow()
        if time.time()-timer>300.0:
            m.save()
            timer=time.time()
        cycle_end=time.time()
        while cycle_end-cycle_start<0.5:
            cycle_end=time.time()

    while mode == 0:

        m.process_maze_string()
        build_marked_maze(m.maze_buffer,[])
        x_pos=m.current_position[0]
        y_pos=m.current_position[1]
        print(m.current_position,"Left:",m.get_node((x_pos,y_pos)).left,", Top:",m.get_node((x_pos,y_pos)).top,", Right:",m.get_node((x_pos+1,y_pos)).left,", Down:",m.get_node((x_pos,y_pos-1)).top)

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
        if i == 'e':
            mode = 2
