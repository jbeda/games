import random

EDGE_OPEN = 0
EDGE_CLOSED = 1

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class MazeCell(object):
  def __init__(self, location):
    self.color = 0
    self.char = None
    self.location = location
    self.border = False
    self.edges = [None, None, None, None]
    self.neighbors = [None, None, None, None]
  
  def edge_state(self, direction):
    if not self.edges[direction]:
      return EDGE_CLOSED
    return self.edges[direction].state

  def __str__(self):
    return '<Cell at %s>' % (self.location)

class MazeEdge(object):
  def __init__(self):
    self.state = EDGE_CLOSED
    
class Maze(object):
  def __init__(self, width, height):
    # The Maze will store set of cells indexed off of position.  We'll pad the
    # cells with a set of border cells that aren't drawn, but make the edge
    # painting algorithms a lot easier.
    self.width = width
    self.height = height
    self.cells = {}  # Keyed off of (x,y)
    
    # Create the cells
    for x in range(-1, width + 1):
      for y in range(-1, height + 1):
        location = (x, y)
        cell = MazeCell(location)
        if x < 0 or x >= width or y < 0 or y >= height:
          cell.border = True
        self.cells[location] = cell
    
    # Create the edges
    for x in range(-1, width + 1):
      for y in range(-1, height + 1):
        cell = self.cells[(x, y)]
        # We only have to add edges going down and right.  The edges to the left/right
        # have already been added by pervious passes.
        if x < width:
          other_cell = self.cells[(x + 1, y)]
          edge = MazeEdge()
          if cell.border and other_cell.border:
            edge.state = EDGE_OPEN
          cell.edges[EAST] = edge
          other_cell.edges[WEST] = edge
          cell.neighbors[EAST] = other_cell
          other_cell.neighbors[WEST] = cell
        if y < height:
          other_cell = self.cells[(x, y + 1)]
          edge = MazeEdge()
          cell.edges[SOUTH] = edge
          if cell.border and other_cell.border:
            edge.state = EDGE_OPEN
          other_cell.edges[NORTH] = edge
          cell.neighbors[SOUTH] = other_cell
          other_cell.neighbors[NORTH] = cell
          
    # Open up the start/end
    self.cells[(0,0)].edges[WEST].state = EDGE_OPEN
    self.cells[(width-1, height-1)].edges[EAST].state = EDGE_OPEN
          
  def __str__(self):
    return '\n'.join([str(c) for c in self.cells.values()])