import maze as mz

class Navigator():

    def __init__(self, maze : mz.Maze):
        self.maze = maze
        self.facing = "up"

    def wallfollow(self):
        maze = self.maze
        maze.process_maze_string()

        adj_nodes = maze.get_adjacent_nodes()

        adj_edges = maze.check_adjacent()
        deadcounter = 0
        for edge in adj_edges:
            if adj_edges[edge] is False:
                deadcounter+=1
        for node in adj_nodes:
            if adj_nodes[node].visit_state == 3:
                deadcounter+=1
        if deadcounter >= 3:
            maze.get_current_node().visit_state=3

        print(", deadcounter:",deadcounter)
        print("facing:",self.facing)

        if self.facing == "left":
            print("debug:",adj_nodes["down"].visit_state != 3,adj_nodes["down"].visit_state)
            if adj_edges["down"]:
                if bool(adj_nodes["down"].visit_state != 3):
                    self.facing="down"
                    maze.move_down()
                else:
                    self.facing="down"
            else:
                self.facing="down"

        elif self.facing == "down":
            print("debug:",adj_nodes["right"].visit_state != 3,adj_nodes["right"].visit_state)
            if adj_edges["right"] and int(adj_nodes["right"].visit_state) != 3:
                self.facing="right"
                maze.move_right()
            else:
                self.facing="right"

        elif self.facing == "right":
            print("debug:",adj_nodes["up"].visit_state != 3,adj_nodes["up"].visit_state)
            if adj_edges["up"] and int(adj_nodes["up"].visit_state) != 3:
                self.facing="up"
                maze.move_up()
            else:
                self.facing="up"

        elif self.facing == "up":
            print("debug:",adj_nodes["left"].visit_state != 3,adj_nodes["left"].visit_state)
            if adj_edges["left"] and int(adj_nodes["left"].visit_state) != 3:
                self.facing="left"
                maze.move_left()
            else:
                self.facing="left"
