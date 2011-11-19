import random

# These are unicode characters for doing box drawing.  The notation here is
# based on the curses naming for these.  It consists of 4 characters looking
# UP, RIGHT, DOWN, LEFT.  A 'B' means blank and an 'S' means stroke (I think).
CP_LIGHT_BOX_BBBB = u'\u00A0'
CP_LIGHT_BOX_BBBS = u'\u2574'
CP_LIGHT_BOX_BBSB = u'\u2577'
CP_LIGHT_BOX_BBSS = u'\u2510'
CP_LIGHT_BOX_BSBB = u'\u2576'
CP_LIGHT_BOX_BSBS = u'\u2500'
CP_LIGHT_BOX_BSSB = u'\u250C'
CP_LIGHT_BOX_BSSS = u'\u252C'
CP_LIGHT_BOX_SBBB = u'\u2575'
CP_LIGHT_BOX_SBBS = u'\u2518'
CP_LIGHT_BOX_SBSB = u'\u2502'
CP_LIGHT_BOX_SBSS = u'\u2524'
CP_LIGHT_BOX_SSBB = u'\u2514'
CP_LIGHT_BOX_SSBS = u'\u2534'
CP_LIGHT_BOX_SSSB = u'\u251C'
CP_LIGHT_BOX_SSSS = u'\u253C'

CP_BOX_MAP = {
  (0, 0, 0, 0): CP_LIGHT_BOX_BBBB,
  (0, 0, 0, 1): CP_LIGHT_BOX_BBBS,
  (0, 0, 1, 0): CP_LIGHT_BOX_BBSB,
  (0, 0, 1, 1): CP_LIGHT_BOX_BBSS,
  (0, 1, 0, 0): CP_LIGHT_BOX_BSBB,
  (0, 1, 0, 1): CP_LIGHT_BOX_BSBS,
  (0, 1, 1, 0): CP_LIGHT_BOX_BSSB,
  (0, 1, 1, 1): CP_LIGHT_BOX_BSSS,
  (1, 0, 0, 0): CP_LIGHT_BOX_SBBB,
  (1, 0, 0, 1): CP_LIGHT_BOX_SBBS,
  (1, 0, 1, 0): CP_LIGHT_BOX_SBSB,
  (1, 0, 1, 1): CP_LIGHT_BOX_SBSS,
  (1, 1, 0, 0): CP_LIGHT_BOX_SSBB,
  (1, 1, 0, 1): CP_LIGHT_BOX_SSBS,
  (1, 1, 1, 0): CP_LIGHT_BOX_SSSB,
  (1, 1, 1, 1): CP_LIGHT_BOX_SSSS,
}

CP_UP_ARROW = u'\u2191'
CP_LEFT_ARROW = u'\u2190'
CP_DOWN_ARROW = u'\u2193'
CP_RIGHT_ARROW = u'\u2192'
CP_WHITE_CIRCLE = u'\u25CB'
CP_BLACK_CIRCLE = u'\u25CF'

def random_wighted_choice(options):
  """Pick a random item of a list based on weights.
  
  Args:
    options: a list of pairs of (weight, value).
  
  Returns:
    One of the values random based on weights."""
  total = reduce(lambda x, t: x+t[0], options, 0)
  rand_pointer = random.uniform(0, total)
  for (weight, value) in options:
    if rand_pointer < weight:
      return value
    else:
      rand_pointer -= weight
  # This shouldn't happen
  return None