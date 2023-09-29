from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from lib.constants import Color, EdgeType
from lib.walk import Walk
from lib.graph import Graph


if TYPE_CHECKING:
  from lib.vertex import Vertex


class AdjacencyList(Graph):

  def __init__(self, *, directed: bool = False):
    super().__init__(directed=directed)
    self.content: list[list[Vertex]] = []

  def append_vertex(self, label: str):
    index = super().append_vertex(label)
    if index == self.vertices[-1].index:
      self.content.append([])
      
    return index

  def remove_vertex(self, iv: int):
    v = self.vertices[iv]
    self.content.pop(iv)
    
    for list in self.content:
      while True:
        try:
          list.remove(v)
        except ValueError:
          break
          
    super().remove_vertex(iv)

  def create_edge(self, ix: int, iy: int, label: Optional[str] = None):
    vx = self.vertices[ix]
    vy = self.vertices[iy]

    self.content[ix].append(vy)
    if not self.directed:
      self.content[iy].append(vx)
    super().create_edge(ix, iy, label)

  def remove_edge(self, ix: int, iy: int, label: Optional[str] = None):
    vx = self.vertices[ix]
    vy = self.vertices[iy]

    if vy not in self.content[ix]:
      return

    self.content[ix].remove(vy)
    if not self.directed:
      self.content[iy].remove(vx)
    super().remove_edge(ix, iy, label)

  def is_neighbor(self, ix: int, iy: int) -> bool:
    return self.vertices[iy] in self.content[ix]

  def is_connected(self):
    """Only works for undirected graphs"""
    for v in self.vertices:
      v.color = Color.WHITE

    def dfs(u: Vertex, parent: Optional[Vertex] = None):
      u.color = Color.GREY
  
      neighbors = self.content[u.index]
      for v in neighbors:
        if v.color == Color.WHITE and v != parent:
          dfs(v, u)
  
      u.color = Color.BLACK
      
    dfs(self.vertices[0])
    for v in self.vertices:
      if v.color == Color.WHITE:
        return False

    return True

  def contains_circuit(self):
    components = self.get_components()
    if (components == 1):
      return len(self.vertices) - 1 != len(self.edges)

    for c in range(components):
      for list in self.content:
        vertices = []
        for v in list:
          if v.component == c:
            vertices.append(v.index)
        subgraph = self.create_induced_subgraph(vertices)
        if (len(subgraph.vertices) - 1 == len(subgraph.edges)):
          return False

    return True

  def get_walk_between(self, source: int, destination: int) -> Optional[Walk]:
    paths = self.get_all_paths_between(source, destination)
    return paths[-1] if paths else None

  # Works only for simple graphs
  def get_all_paths_between(self, source: int, destination: int) -> list[Walk]:
    length = len(self.vertices)
    if source >= length or destination >= length:
      return None

    paths: list[Walk] = []
    currentPath: list[int] = [source]
    u = self.vertices[source]
    v = self.vertices[destination]

    def dfs(source: Vertex, destination: Vertex):
      if source.index == destination.index:
        path = Walk(self, currentPath)
        paths.append(path)
        return

      source.color = Color.BLACK
      neighbors = self.content[source.index]

      for v in neighbors:
        if v.color == Color.BLACK:
          continue

        currentPath.append(v.index)
        dfs(v, destination)
        currentPath.pop()

      source.color = Color.WHITE
      return

    for v in self.vertices:
      v.color = Color.WHITE

    dfs(u, v)

    return paths

  def find_cycle(self) -> Optional[Walk]:
    for v in self.vertices:
      v.color = Color.WHITE

    def dfs(u: Vertex, parent: Vertex, walk: list[int]) -> bool:
      u.color = Color.BLACK
      neighbors = self.content[u.index]
      for v in neighbors:
        if v.color == Color.WHITE:
          walk.append(v.index)
          if dfs(v, u, walk):
            return True
          else:
            walk.pop()
        elif v != parent:
          walk.append(v.index)
          return True

      return False

    for v in self.vertices:
      if v.color != Color.WHITE:
        continue

      walk = [v.index]
      if dfs(v, None, walk):
        start = walk[:-1].index(walk[-1])
        cycle = walk[start:]
        return Walk(self, cycle)

    return None

  def get_cycle_from_circuit(self, circuit: Walk, edge: tuple[int, int, Optional[str]]) -> Walk:
    u = self.vertices[edge[0]]
    v = self.vertices[edge[1]]
    cycle = [u.index]

    def dfs(source: Vertex, destination: Vertex):
      if source.index == destination.index:
        return True

      source.color = Color.BLACK
      neighbors = self.content[source.index]

      for w in neighbors:
        if w.color == Color.BLACK:
          continue

        cycle.append(w.index)
        if dfs(w, destination):
          return True
        cycle.pop()

      return False

    for w in self.vertices:
      w.color = Color.WHITE

    dfs(u, v)
    cycle.append(u.index)
    print(cycle)

    return Walk(self, cycle)

  def restricted_find_cycle(self) -> Walk:
    if any(v.degree < 2 for v in self.vertices):
      raise Exception("Enter a graph G such that g(v) >= 2 for all v belonging to VG")

    for v in self.vertices:
      v.color = Color.WHITE

    source = self.vertices[0]
    path = [source.index, self.content[source.index][1].index]

    def dfs(current: Vertex, parent: Vertex):
      if parent != source and current == source:
        return True

      current.color = Color.BLACK
      neighbors = self.content[current.index][1:]

      for v in neighbors:
        if v.color == Color.BLACK:
          continue

        path.append(v.index)
        if dfs(v, current):
          return True
        path.pop()

      current.color = Color.WHITE
      return False

    dfs(self.content[source.index][1], source)

    return Walk(self, path)

  def low_link_values(self):
    if not self.directed:
      raise Exception("Not a digraph")

    length = len(self.vertices)
    low = [0] * length
    disc = [0] * length
    self.time = 0

    for v in self.vertices:
      v.color = Color.WHITE

    def dfs(u, low, disc):
      u.color = Color.GREY
      low[u.index] = self.time
      disc[u.index] = self.time
      self.time += 1

      neighbors = self.content[u.index]
      for v in neighbors:
        if v.color == Color.WHITE:
          dfs(v, low, disc)
          low[u.index] = min(low[u.index], low[v.index])
        else:
          low[u.index] = min(low[u.index], disc[v.index])

      u.color = Color.BLACK

    for v in self.vertices:
      if (v.color == Color.WHITE):
        dfs(v, low, disc)

    del self.time
    return low

  def strongly_connected_components(self):
    if not self.directed:
      raise Exception("Not a digraph")

    length = len(self.vertices)
    low = [0] * length
    disc = [0] * length
    stack = [False] * length
    self.time = 0

    for v in self.vertices:
      v.color = Color.WHITE

    def dfs(u, low, disc):
      u.color = Color.GREY
      low[u.index] = self.time
      disc[u.index] = self.time
      stack[u.index] = True
      self.time += 1

      neighbors = self.content[u.index]
      for v in neighbors:
        if v.color == Color.WHITE:
          dfs(v, low, disc)
          low[u.index] = min(low[u.index], low[v.index])
        elif stack[v.index]:
          low[u.index] = min(low[u.index], disc[v.index])

      u.color = Color.BLACK
      stack[u.index] = False

    for v in self.vertices:
      if (v.color == Color.WHITE):
        dfs(v, low, disc)

    del self.time

    arranged_low = sorted(zip(low, range(length)))
    counter = 0
    components = [[self.vertices[arranged_low[0][1]]]]
    for i in range(1, length):
      if arranged_low[i - 1][0] != arranged_low[i][0]:
        counter += 1
        components.append([])
        
      components[counter].append(self.vertices[arranged_low[i][1]])
    
    return components

  def topological_sort(self):
    stack: list[Vertex] = []
    
    for v in self.vertices:
      v.color = Color.WHITE

    def dfs(u: Vertex, stack: list[Vertex]):
      u.color = Color.GREY
  
      neighbors = self.content[u.index]
      for v in neighbors:
        if v.color == Color.WHITE:
          dfs(v, stack)

      stack.append(u)
      u.color = Color.BLACK

    for v in self.vertices:
      if v.color is Color.WHITE:
        dfs(v, stack)

    return stack

  def depth_first_search(self):
    values = {
      "Tree Edges": [],
      "Back Edges": [],
      "Push Counter": 1,
      "Pop Counter": 1,
      "Components": 0
    }

    for v in self.vertices:
      v.color = Color.WHITE
    
    def dfs(u: Vertex, parent: Optional[Vertex] = None):
      u.color = Color.GREY
      u.component = values["Components"]
  
      u.entry_depth = values["Push Counter"]
      values["Push Counter"] += 1
  
      neighbors = self.content[u.index]
      for v in neighbors:
        if v == parent:
          continue

        edge = (u, v)
        edge = next(filter(lambda e: e == edge, self.edges))
        if v.color == Color.WHITE:
          edge.type = EdgeType.TREE_EDGE
          values["Tree Edges"].append(edge)
          dfs(v, u)
        elif v.color == Color.GREY:
          edge.type = EdgeType.BACK_EDGE
          values["Back Edges"].append(edge)
  
      u.exit_depth = values["Pop Counter"]
      values["Pop Counter"] += 1
  
      u.color = Color.BLACK
      
    for v in self.vertices:
      if v.color == Color.WHITE:
        dfs(v)
        values["Components"] += 1

    return values

  @staticmethod
  def create_empty_graph(n: int, *, directed: bool = False) -> Graph:
    return Graph.create_empty_graph(n, graph_type=AdjacencyList, directed=directed)

  @staticmethod
  def create_complete_graph(n: int) -> Graph:
    return Graph.create_complete_graph(n, graph_type=AdjacencyList)

  @staticmethod
  def create_regular_graph(n: int, k: int) -> Graph:
    return Graph.create_regular_graph(n, k, graph_type=AdjacencyList)
    
  @staticmethod
  def is_2satisfiable(elements: list[tuple[int, int]]) -> bool:
    return Graph.is_2satisfiable(elements, graph_type=AdjacencyList)
