from lib.constants import Color


class Vertex:

  def __init__(self, index: int, label: str):
    self.index: int = index
    self.label: str = label
    self.color: Color = Color.WHITE
    self.degree: int = 0
    self.component: int = 0
    self.entry_depth: int = 0
    self.exit_depth: int = 0

  def __iter__(self):
    yield self.label
    yield self.degree

  def __str__(self):
    return str(tuple(self))

  def __eq__(self, __value: object) -> bool:
    if isinstance(__value, Vertex):
      return self is __value

    if isinstance(__value, int):
      return self.index == __value

    if isinstance(__value, str):
      return self.label == __value

    return False
