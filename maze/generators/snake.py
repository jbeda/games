from model import *
from util import *
import curses

class SnakeGenerator(object):
  def __init__(self, maze, redraw):
    self.maze = maze
    self.redraw = redraw
    
  def generate(self):
    c = self.maze.cells[(0,0)]
    # dir_char = ord('>')
    dir_char = CP_RIGHT_ARROW
    dir = EAST
    while True:
      if not c.neighbors[dir].border:
        c.edges[dir].state = EDGE_OPEN
        c.char = dir_char
        c = c.neighbors[dir]
      elif not c.neighbors[SOUTH].border:
        c.edges[SOUTH].state = EDGE_OPEN
        c.char = CP_DOWN_ARROW
        c = c.neighbors[SOUTH]
        if dir == EAST:
          dir = WEST
          dir_char = CP_LEFT_ARROW
        else:
          dir = EAST
          dir_char = CP_RIGHT_ARROW
      else:
        break
      self.redraw()