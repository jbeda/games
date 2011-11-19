#! /usr/bin/env python

import string
from collections import deque

# DICTIONARY="/usr/share/dict/words"
DICTIONARY="/Users/jbeda/bin/TWL06.txt"

class HashDictionary(object):
  def __init__(self, word_length, file=DICTIONARY):
    """Load up the dictionary from a file."""
    self.d = set()
    f = open(file)
    for w in f.readlines():
      w = w.strip().lower()
      if len(w) == word_length:
        self.d.add(w)

  def find_edges(self, word):
    """Find all adjacent words according to WordGolf rules"""
    ret = []
    for i in range(len(word)):
      for c in string.lowercase:
        if c != word[i]:
          new_word = word[:i] + c + word[i+1:]
          if new_word in self.d:
            ret.append(new_word)
    return ret

def decode_path(parents, end):
  item = end
  path = []
  while item != None:
    path.append(item)
    item = parents[item]
  return reversed(path)

def find_path(start, end):
  """Find the shortest path from start to end"""
  print "Building Dictionary"
  d = HashDictionary(len(start))
  print "Dictionary Built.  %d entries" % len(d.d)

  q = deque()
  visited = { start: None }
  q.appendleft(start)
  
  i = 0
  found = []
  while len(q) and not found:
    i += 1
    item = q.pop()
    edges = d.find_edges(item)
    # print "I: %d Q: %d W: %s E: %s" % (i, len(q), item, ", ".join(edges))
    if item == end:
      found =  decode_path(visited, end)
    for e in edges:
      if e in visited:
        continue
      visited[e] = item
      q.appendleft(e)
  print "BFS Iterations: %d" % (i,)
  return found
  
print "Computing path"
path = find_path("work", "play")
print " -> ".join(path)
