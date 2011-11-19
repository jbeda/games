#!/usr/bin/python

import curses
import random

from model import *
from generators import *
from util import *
  
class MazeScreen(object):
  def __init__(self, screen, width, height):
    self.screen = screen
    self.width = width
    self.height = height
    self.reset_maze() 
    
  def reset_maze(self):
    self.maze = Maze(self.width, self.height)
  
  @staticmethod
  def color_attr(color):
    n = color + 1
    curses.init_pair(n, color, curses.COLOR_BLACK)
    return curses.color_pair(n)
    
  def redraw(self):
    self.screen.erase()

    # As we draw, we have a grid of 2x2 chars that are interesting:
    # +-
    # |c
    # Where + is a corner, - and | are edges and c is a cell
    for x in range(self.maze.width + 1):
      for y in range(self.maze.height + 1):
        (base_x, base_y) = (x * 2, y * 2)
        cell = self.maze.cells[(x, y)]
        
        # Draw the corner
        self.draw_ul_corner(base_x, base_y, cell)
        
        # Draw the north edge
        if cell.edge_state(NORTH) == EDGE_CLOSED:
          self.screen.addstr(base_y, base_x + 1, CP_LIGHT_BOX_BSBS.encode('utf_8'))
          
        # Draw the west edge
        if cell.edge_state(WEST) == EDGE_CLOSED:
          self.screen.addstr(base_y + 1, base_x, CP_LIGHT_BOX_SBSB.encode('utf_8'))
          
        # Draw the cell
        if cell.char:
          output = cell.char
          if isinstance(output, unicode):
            output = output.encode('utf_8')
          self.screen.addstr(base_y + 1, base_x + 1, output)
          
    self.screen.refresh()
  
  def draw_ul_corner(self, x, y, cell):
    key = [0, 0, 0, 0]
    
    key[EAST] = cell.edge_state(NORTH) == EDGE_CLOSED
    key[SOUTH] = cell.edge_state(WEST) == EDGE_CLOSED
    if cell.neighbors[NORTH]:
      key[NORTH] = cell.neighbors[NORTH].edge_state(WEST) == EDGE_CLOSED
    if cell.neighbors[WEST]:
      key[WEST] = cell.neighbors[WEST].edge_state(NORTH) == EDGE_CLOSED
    ch = CP_BOX_MAP[tuple(key)]
    if ch:
      self.screen.addstr(y, x, ch.encode('utf_8'))
      
  def slow_redraw(self):
    self.redraw()
    curses.napms(10)
  
  def main(self):
    try:
      curses.curs_set(0)
    except curses.error:
      pass
    self.redraw()
    while 1:
      key = self.screen.getch()
      if key == ord('r'): self.redraw()
      if key == ord('g'):
        self.reset_maze()
        self.redraw()
        key = self.screen.getch()
        gen = None
        if key == ord('s'):
          gen = SnakeGenerator(self.maze, self.slow_redraw)
        if key == ord('g'):
          gen = GrowingTreeGenerator(self.maze, self.slow_redraw)
        if gen:
          gen.generate()
      elif key == ord('q'): break
      
def main(stdscr):
  #  curses.use_default_colors()
  screen = MazeScreen(stdscr, 20, 20)
  screen.main()

if __name__ == '__main__':
  import locale
  locale.setlocale(locale.LC_ALL, '')
  curses.wrapper(main)
