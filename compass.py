from constants import *
import time
import maze

class Navigator():

    def __init__(self, maze):
        self.maze = maze
        self.facing = "up"

    def wallfollow(self):
        maze = self.maze
        if self.facing == "left":
            if maze.check_down():
                self.facing="down"
                maze.move_down()
            else:
                self.facing="down"

        if self.facing == "down":
            if maze.check_right():
                self.facing="right"
                maze.move_right()
            else:
                self.facing="right"

        if self.facing == "right":
            if maze.check_up():
                self.facing="up"
                maze.move_up()
            else:
                self.facing="up"

        if self.facing == "up":
            if maze.check_left():
                self.facing="left"
                maze.move_left()
            else:
                self.facing="left"

        

