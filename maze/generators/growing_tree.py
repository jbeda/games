from model import *
from util import *

import random

class GrowingTreeGenerator(object):
  def __init__(self, maze, redraw):
    self.maze = maze
    self.redraw = redraw
    self.working_cells = None
    
  def generate(self):
    for c in self.maze.cells.values():
      if not c.border:
        c.char = CP_BLACK_CIRCLE

    # pick a cell at random
    start_cell = self.maze.cells[
      (random.randrange(self.maze.width), random.randrange(self.maze.height))]
    start_cell.color = 1
    start_cell.char = CP_WHITE_CIRCLE
    self.working_cells = [start_cell]
    self.redraw()
    while len(self.working_cells):
      c = self.pick_cell()
      (dir, n) = self.find_unvisited_neighbor(c)
      if not n:
        self.working_cells.remove(c)
        c.color = 2
        c.char = None
      else:
        self.working_cells.append(n)
        n.color = 1
        n.char = CP_WHITE_CIRCLE
        c.edges[dir].state = EDGE_OPEN
      self.redraw()
      
  def pick_cell(self):
    weighted_options = [
      (0.1, self.pick_random_cell),
      (0.9, self.pick_newest_cell)
    ]
    option = random_wighted_choice(weighted_options)
    return option() 
      
  def pick_newest_cell(self):
    return self.working_cells[-1]
    
  def pick_random_cell(self):
    return random.choice(self.working_cells)
    
  def find_unvisited_neighbor(self, c):
    candidates = []
    for (dir, n) in enumerate(c.neighbors):
      if n.border: continue
      if not n.color:
        candidates.append((dir, n))
    if not candidates:
      return (None, None)
    return random.choice(candidates)