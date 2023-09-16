from __future__ import annotations
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
  from lib.graph import Graph


class Walk:
  """Only works for simple graphs"""

  def __init__(self, graph: Graph, vertices: list[int]):
    if not graph.validate_vertices(list(set(vertices))) or len(vertices) == 0:
      raise Exception("Invalid vertices")

    self.graph = graph
    self.vertices = [graph.vertices[v] for v in vertices]
    self.length = len(self.vertices) - 1

    self.edges = []
    for i in range(self.length):
      edge = (vertices[i], vertices[i + 1])
      try:
        index = graph.edges.index(edge)
      except ValueError:
        raise Exception("Invalid Walk") from None
      self.edges.append(graph.edges[index])

    self.content = []
    for v, e in zip(self.vertices, self.edges):
      self.content.append(str(v))
      self.content.append(str(e))
    self.content.append(str(self.vertices[-1]))

  def get_primitive(self, reverse: bool = False):
    if reverse:
      return self.content[::-1]

    return self.content

  def get_path(self) -> Walk:
    last = -1

    for i, v in enumerate(self.vertices):
      if v in self.vertices[:i]:
        break
      last += 1

    return self.section(0, last)

  def section(self, i: int, j: int) -> Optional[Walk]:
    if not (0 <= i < j < self.length):
      return None

    sublist = [v.index for v in self.vertices[i:(j + 1)]]
    return Walk(self.graph, sublist)
