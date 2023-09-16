from enum import Enum, auto


class Color(Enum):
  WHITE = auto(),
  GREY = auto(),
  BLACK = auto(),


class EdgeType(Enum):
  UNCLASSIFIED = auto(),
  TREE_EDGE = auto(),
  BACK_EDGE = auto(),
  CROSS_EDGE = auto(),
  FOWARD_EDGE = auto(),