from __future__ import annotations
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
  from lib.vertex import Vertex


class Edge:

  def __init__(self, u: Vertex, v: Vertex, label: Optional[str] = None, *, directed: bool = False):
    self.directed = directed

    ends: tuple[Vertex, Vertex] = (u, v)
    if not directed and u.index < v.index:
      ends = (v, u)

    self.ends = ends
    self.label = label

  def contains(self, v: Vertex) -> bool:
    return v.index == self.ends[0].index or v.index == self.ends[1].index

  def __eq__(self, __value: object) -> bool:
    if isinstance(__value, Edge):
      return self is __value

    if isinstance(__value, tuple):
      if not (2 <= len(__value) <= 3):
        return False

      if len(__value) == 3 and __value[2] != None:
        return self.label == __value[2]

      if not self.directed:
        __value = __value[::-1] if __value[1] < __value[0] else __value
        
      return self.ends[0].index == __value[0] and self.ends[1].index == __value[1]

    return False

  def __iter__(self):
    for v in self.ends:
      yield v.label

  def __str__(self):
    if self.label is None:
      return str(tuple(self))

    return self.label + str(tuple(self))

