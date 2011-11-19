#! /usr/bin/env python

import time

verbose = False

class Cell:
  def __init__(self, coord):
    self.sequences = []
    self.value = 0
    self.constraints = 0
    self.coord = coord
    
  def SetValue(self, value):
    """Sets the value of this cell.  
    
    Returns True if this results in the board being in a state such that no 
    solution exists. (A deadend board)"""
    if verbose:
      print "Setting %s to %d" % (self.coord, value)
      print board
    if self.value != 0:
      raise Exception("Value already set on Cell (%d)" % self.value)
    if ValueToBit(value) & self.constraints:
      raise Exception("Value breaks constraints (%x)" % self.constraints)
    self.value = value;
    deadend = False
    for seq in self.sequences:
      deadend = deadend or seq.NoteNumberUsed(value)
    return deadend
  
  def ClearValue(self):
    """Clears the value of the cell, updating constraints and sequences."""
    if verbose:
      print "Clearing %s from %d" % (self.coord, self.value)
      print board
    for seq in self.sequences:
      seq.ClearNumberUsed(self.value)
    self.value = 0
      
  def UpdateConstraint(self):
    """Caches the current constraints on this cell.
    
    Returns True if this cell has no value set and is overconstrained. 
    (A deadend board)"""
    self.constraints = 0
    for seq in self.sequences:
      self.constraints |= seq.values_used
    if self.value == 0 and self.constraints == 0x1ff:
      return True
    return False
  
class Sequence:
  def __init__(self):
    self.cells = []
    self.values_used = 0
    
  def NoteNumberUsed(self, value):
    """Note that this number is used in the sequence.  
    
    Returns true if this results in a deadend board."""
    if ValueToBit(value) & self.values_used:
      raise Exception("Value already used")
    self.values_used |= ValueToBit(value)
    
    deadend = False
    for cell in self.cells:
      deadend = deadend or cell.UpdateConstraint()
    return deadend
    
  def ClearNumberUsed(self, value):
    self.values_used &= ~ValueToBit(value)
    self.values_used &= 0x1ff
    for cell in self.cells:
      cell.UpdateConstraint()
    
def ValueToBit(value):
  return 1 << (value - 1)

def MaskToOpenValues(mask):
  ret = []
  for i in range(9):
    if not ((mask >> i) & 1):
      ret.append(i+1)
  return ret
  
def BitsSet(mask):
  bits_set = 0
  for i in range(9):
    bits_set += mask & 1
    mask >>= 1
  return bits_set
  
def MaskString(mask):
  ret = ""
  for i in range(9):
    if ((mask >> i) & 1):
      ret += "%d " % (i+1,)
    else:
      ret += "- "
  return ret
  
class Board:
  def __init__(self, input):  
    # create cells
    cells = self.cells = []
    for iRow in range(9):
      cells.append([])
      for iCol in range(9):
        cells[iRow].append(Cell((iRow, iCol)))

    # create row Sequences
    for iRow in range(9):
      seq = Sequence()
      for iCol in range(9):
        cells[iRow][iCol].sequences.append(seq)
        seq.cells.append(cells[iRow][iCol])

    # create col Sequences
    for iCol in range(9):
      seq = Sequence()
      for iRow in range(9):
        cells[iRow][iCol].sequences.append(seq)
        seq.cells.append(cells[iRow][iCol])

    # create subsection Sequences
    for iSectionRow in range(3):
      for iSectionCol in range(3):
        seq = Sequence()
        iRowBase = iSectionRow * 3
        iColBase = iSectionCol * 3
        for iRowDelta in range(3):
          for iColDelta in range(3):
            cell = cells[iRowBase + iRowDelta][iColBase + iColDelta]
            cell.sequences.append(seq)
            seq.cells.append(cell)
        
    # set up board:
    count = 0
    for c in input:
      if c.isspace():
        continue
      if c != '-':
        iRow = count/9
        iCol = count%9
        cell = cells[iRow][iCol]
        cell.SetValue(int(c))
      count += 1
      
    self.solve_iterations = 0
      
  def __str__(self):
    output = "+-------+-------+-------+\n"
    for iRow in range(9):
      output += "| "
      for iCol in range(9):
        value = self.cells[iRow][iCol].value
        if value == 0:
          output += "  "
        else:
          output += "%d " % value
        if iCol % 3 == 2:
          output += "| "
      output += "\n"
      if iRow % 3 == 2:
        output += "+-------+-------+-------+\n"
    return output    
    
  def Solve(self):
    """Solve the puzzle.
    
    If the puzzle can be solved, this function will return True and have
    the state represent the solution.  If the puzzle cannot be solved it will
    return False and leave the state unchanged."""
    self.solve_iterations += 1
    # First pick a cell
    cell = self.FindMostConstrainedCell()
    #cell = self.FindNextCell()
    if cell == None:
      return True
    
    for value in MaskToOpenValues(cell.constraints):
      deadend = cell.SetValue(value)
      if not deadend:
        if self.Solve():
          return True
      cell.ClearValue()
    return False
  
  def FindNextCell(self):
    """Find the next cell to try solve with.
    
    Simple greedy algorithm that takes the first cell without a value."""
    for iRow in range(9):
      for iCol in range(9):
        cell = self.cells[iRow][iCol]
        if cell.value == 0:
          return cell        


  def FindMostConstrainedCell(self):
    """Find the next cell to try solve with.

    Finds the most constrained cell first as it will have the smallest
    branching factor."""
    max_bits_set = 0
    max_bits_cell = None
    for iRow in range(9):
      for iCol in range(9):
        cell = self.cells[iRow][iCol]
        if cell.value == 0:
          bits_set = BitsSet(cell.constraints)
          if bits_set > max_bits_set:
            max_bits_set = bits_set
            max_bits_cell = cell
    return max_bits_cell
          
      
input1 = """
-795---26
----9-1--  
1-84-2---
--687---9
8--9-4--1
4---513--
---1-95-2
--1-3----
92---681-
"""

input2 = """
--9748---
7--------
-2-1-9---
--7---24-
-64-1-59-
-98---3--
---8-3-2-
--------6
---2759--
"""

board = ""
board = Board(input2)
print board
print "Solving..."
t1 = time.time()
solved = board.Solve()
t2 = time.time()

if solved:
  print "SOLVED!"
else:
  print "NOT SOLVED!"

print 'Solving took %0.3f ms' % ((t2-t1)*1000.0,)

print "Used %d iterations" % board.solve_iterations
print board
