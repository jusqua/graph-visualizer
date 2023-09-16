from typing import Optional
from lib.graph import Graph


class AdjacencyMatrix(Graph):
  """Deprecated, most of methods are not implemented"""

  def __init__(self):
    super().__init__()
    self.content: list[list[int]] = []

  def append_vertex(self, label: str):
    super().append_vertex(label)
    for row in self.content:
      row.append(0)
    self.content.append([0] * len(self.vertices))

  def create_edge(self, ix: int, iy: int, label: Optional[str] = None):
    self.content[ix][iy] += 1
    if not self.directed:
      self.content[iy][ix] += 1
    super().create_edge(ix, iy, label)

  def remove_edge(self, ix: int, iy: int, label: Optional[str] = None):
    if (self.content[ix][iy] == 0):
      return

    self.content[ix][iy] -= 1
    if not self.directed:
      self.content[iy][ix] -= 1
    super().remove_edge(ix, iy, label)

  def is_neighbor(self, ix: int, iy: int) -> bool:
    return bool(self.content[ix][iy])
