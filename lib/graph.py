from __future__ import annotations
from typing import Optional
from copy import deepcopy
from enum import Enum


class Color(Enum):
  white = 1,
  grey = 2,
  black = 3,


class Vertex:

  def __init__(self, index: int, label: str):
    self.index: int = index
    self.label: str = label
    self.color: Color = Color.white
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


class Edge:

  def __init__(self, u: Vertex, v: Vertex, label: Optional[str] = None):
    self.ends: tuple[Vertex, Vertex] = (u, v) if u.index < v.index else (v, u)
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

      __value = __value[::-1] if __value[1] < __value[0] else __value
      return self.ends[0].index == __value[0] and self.ends[
        1].index == __value[1]

    return False

  def __iter__(self):
    for v in self.ends:
      yield v.label

  def __str__(self):
    if self.label is None:
      return str(tuple(self))

    return self.label + str(tuple(self))


class Graph:

  def __init__(self):
    self.vertices: list[Vertex] = []
    self.edges: list[Edge] = []

  def append_vertex(self, label: str):
    index = len(self.vertices)
    self.vertices.append(Vertex(index, label))

  def create_edge(self, ix: int, iy: int, label: Optional[str] = None):
    vx = self.vertices[ix]
    vy = self.vertices[iy]

    vx.degree += 1
    vy.degree += 1

    self.edges.append(Edge(vx, vy, label))

  def remove_edge(self, ix: int, iy: int, label: Optional[str] = None):
    primitive = (ix, iy, label)
    edge = list(filter(lambda e: e == primitive, self.edges))

    if len(edge) == 0:
      return

    self.edges.remove(edge[0])

    vx = self.vertices[ix]
    vy = self.vertices[iy]

    vx.degree -= 1
    vy.degree -= 1

  def get_degree(self, index: int) -> int:
    return self.vertices[index].degree

  def is_neighbor(self, ix: int, iy: int) -> bool:
    del ix, iy
    return False

  def is_bipartite(self, x: list[int], y: list[int]) -> bool:
    if set(x).intersection(y):
      return False

    union = set(x) | set(y)
    vertices = set(map(lambda n: n.index, self.vertices))
    if union != vertices:
      return False

    for subgraph in (x, y):
      for n, i in enumerate(subgraph):
        for j in subgraph[n:]:
          if self.is_neighbor(i, j):
            return False

    return True

  def validate_vertices(self, vertices: list[int]) -> bool:
    if len(set(vertices)) != len(vertices):
      return False

    return all(v in self.vertices for v in vertices)

  def validate_edges(self, edges: list[tuple[int, int,
                                             Optional[str]]]) -> bool:
    if len(set(edges)) != len(edges):
      return False

    return all(e in self.edges for e in edges)

  def subtract_vertices(self, vertices: list[int]) -> Graph | None:
    if not self.validate_vertices(vertices):
      return None

    g = type(self)()
    equivalent_vertices = []

    for v in self.vertices:
      if v not in vertices:
        g.append_vertex(v.label)
        equivalent_vertices.append((v.index, g.vertices[-1].index))

    for e in self.edges:
      edge = []

      for old, new in equivalent_vertices:
        if old in e.ends:
          edge.append(new)

      if len(edge) == 2:
        g.create_edge(*edge, e.label)

    return g

  def subtract_edges(
      self, edges: list[tuple[int, int, Optional[str]]]) -> Graph | None:
    if not self.validate_edges(edges):
      return None

    g = deepcopy(self)

    for e in edges:
      g.remove_edge(*e)

    return g

  def create_induced_subgraph(self, vertices: list[int]) -> Graph | None:
    if not self.validate_vertices(vertices):
      return None

    g = type(self)()
    equivalent_vertices = []

    for v in self.vertices:
      if v in vertices:
        g.append_vertex(v.label)
        equivalent_vertices.append((v.index, g.vertices[-1].index))

    for e in self.edges:
      edge = []

      for old, new in equivalent_vertices:
        if old in e.ends:
          edge.append(new)

      if len(edge) == 2:
        g.create_edge(*edge, e.label)

    return g

  def create_edge_induced_subgraph(
      self, edges: list[tuple[int, int, Optional[str]]]) -> Graph | None:
    if not self.validate_edges(edges):
      return None

    g = type(self)()
    equivalent_vertices = []

    for e in self.edges:
      if e not in edges:
        continue

      for v in e.ends:
        if not any(old == v for old, _ in equivalent_vertices):
          g.append_vertex(v.label)
          equivalent_vertices.append((v.index, g.vertices[-1].index))

      edge = []
      for old, new in equivalent_vertices:
        if old in e.ends:
          edge.append(new)

      g.create_edge(*edge, e.label)

    return g

  def create_subgraph(
      self, vertices: list[int],
      edges: list[tuple[int, int, Optional[str]]]) -> Graph | None:
    if not (self.validate_vertices(vertices) and self.validate_edges(edges)):
      return None

    g = type(self)()
    equivalent_vertices = []

    for v in self.vertices:
      if v in vertices:
        g.append_vertex(v.label)
        equivalent_vertices.append((v.index, g.vertices[-1].index))

    for e in edges:
      edge = []

      for old, new in equivalent_vertices:
        if old in e:
          edge.append(new)

      if len(edge) == 2:
        label = e[2] if len(e) == 3 else None
        g.create_edge(*edge, label)

    return g

  def dfs(self):
    return

  @staticmethod
  def create_empty_graph(n: int, graph_type: type[Graph]) -> Graph:
    g = graph_type()

    for i in range(n):
      g.append_vertex(f"v{i + 1}")

    return g

  @staticmethod
  def create_complete_graph(n: int, graph_type: type[Graph]) -> Graph:
    kn = Graph.create_empty_graph(n, graph_type)

    for i in range(n):
      for j in range(i + 1, n):
        kn.create_edge(i, j)

    return kn

  @staticmethod
  def create_regular_graph(n: int, k: int, graph_type: type[Graph]) -> Graph:
    if (n * k) % 2:
      return None

    g = Graph.create_empty_graph(n, graph_type)
    for d in range(k):
      for i in range(d % 2, n, 2):
        g.create_edge(i, (i + 1) % n)

    return g

  def __str__(self):
    edges_list = [str(e) for e in self.edges]
    vertices = [tuple(v) for v in self.vertices]
    total_degree = sum([v.degree for v in self.vertices])
    odd_degree_vertices = len([v for v in self.vertices if v.degree % 2])
    even_degree_vertices = len(self.vertices) - odd_degree_vertices

    return f"Number of vertices: {len(self.vertices)}\n" + \
           f"Vertices (label, degree): {vertices}\n" + \
           f"Odd Degree Vertices: {odd_degree_vertices}\n" + \
           f"Even Degree Vertices: {even_degree_vertices}\n" + \
           f"Total Degree: {total_degree}\n" + \
           f"Number of edges: {len(edges_list)}\n" + \
           f"Edges: {edges_list}\n"


class AdjacencyMatrix(Graph):

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
    self.content[iy][ix] += 1
    super().create_edge(ix, iy, label)

  def remove_edge(self, ix: int, iy: int, label: Optional[str] = None):
    if (self.content[ix][iy] == 0):
      return

    self.content[ix][iy] -= 1
    self.content[iy][ix] -= 1
    super().remove_edge(ix, iy, label)

  def is_neighbor(self, ix: int, iy: int) -> bool:
    return bool(self.content[ix][iy])


class AdjacencyList(Graph):

  def __init__(self):
    super().__init__()
    self.content: list[list[Vertex]] = []

  def append_vertex(self, label: str):
    super().append_vertex(label)
    self.content.append([self.vertices[-1]])

  def create_edge(self, ix: int, iy: int, label: Optional[str] = None):
    vx = self.vertices[ix]
    vy = self.vertices[iy]

    self.content[ix].append(vy)
    self.content[iy].append(vx)
    super().create_edge(ix, iy, label)

  def remove_edge(self, ix: int, iy: int, label: Optional[str] = None):
    vx = self.vertices[ix]
    vy = self.vertices[iy]

    if vy not in self.content[ix]:
      return

    self.content[ix].remove(vy)
    self.content[iy].remove(vx)
    super().remove_edge(ix, iy, label)

  def is_neighbor(self, ix: int, iy: int) -> bool:
    return self.vertices[iy] in self.content[ix][1:]

  def is_connected(self):
    for v in self.vertices:
      v.color = Color.white

    self.__dfs(self.vertices[0], None)
    for v in self.vertices[1:]:
      if v.color == Color.white:
        return False

    return True

  def get_components(self):
    self.dfs()
    return self.components

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

      source.color = Color.black
      neighbors = self.content[source.index][1:]

      for v in neighbors:
        if v.color == Color.black:
          continue

        currentPath.append(v.index)
        dfs(v, destination)
        currentPath.pop()

      source.color = Color.white
      return

    for v in self.vertices:
      v.color = Color.white

    dfs(u, v)

    return paths

  def find_cycle(self) -> Optional[Walk]:
    for v in self.vertices:
      v.color = Color.white

    def dfs(u: Vertex, parent: Vertex, walk: list[int]) -> bool:
      u.color = Color.black
      neighbors = self.content[u.index][1:]
      for v in neighbors:
        if v.color == Color.white:
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
      if v.color != Color.white:
        continue

      walk = [v.index]
      if dfs(v, None, walk):
        start = walk[:-1].index(walk[-1])
        cycle = walk[start:]
        return Walk(self, cycle)

    return None

  def get_cycle_from_circuit(self, circuit: Walk,
                             edge: tuple[int, int, Optional[str]]) -> Walk:
    u = self.vertices[edge[0]]
    v = self.vertices[edge[1]]
    cycle = [u.index]

    def dfs(source: Vertex, destination: Vertex):
      if source.index == destination.index:
        return True

      source.color = Color.black
      neighbors = self.content[source.index][1:]

      for w in neighbors:
        if w.color == Color.black:
          continue

        cycle.append(w.index)
        if dfs(w, destination):
          return True
        cycle.pop()

      return False

    for w in self.vertices:
      w.color = Color.white

    dfs(u, v)
    cycle.append(u.index)
    print(cycle)

    return Walk(self, cycle)

  def restricted_find_cycle(self) -> Walk:
    if any(v.degree < 2 for v in self.vertices):
      raise Exception(
        "Enter a graph G such that g(v) >= 2 for all v belonging to VG")

    for v in self.vertices:
      v.color = Color.white

    source = self.vertices[0]
    path = [source.index, self.content[source.index][1].index]

    def dfs(current: Vertex, parent: Vertex):
      if parent != source and current == source:
        return True

      current.color = Color.black
      neighbors = self.content[current.index][2:]

      for v in neighbors:
        if v.color == Color.black:
          continue

        path.append(v.index)
        if dfs(v, current):
          return True
        path.pop()

      current.color = Color.white
      return False

    dfs(self.content[source.index][1], source)

    return Walk(self, path)

  def dfs(self):
    self.tree_edges = []
    self.back_edges = []

    self.push_counter = 1
    self.pop_counter = 1

    for v in self.vertices:
      v.color = Color.white

    self.components = 0
    for v in self.vertices:
      if v.color == Color.white:
        self.__dfs(v, None)
        self.components += 1

  def __dfs(self, u: Vertex, parent: Vertex):
    u.color = Color.grey
    u.component = self.components

    u.entry_depth = self.push_counter
    self.push_counter += 1

    neighbors = self.content[u.index][1:]
    for v in neighbors:
      if v == parent:
        continue

      edge = Edge(u, v)
      if v.color == Color.white:
        self.tree_edges.append(edge)
        self.__dfs(v, u)
      elif v.color == Color.grey:
        self.back_edges.append(edge)

    u.exit_depth = self.pop_counter
    self.pop_counter += 1

    u.color = Color.black

  @staticmethod
  def create_empty_graph(n: int) -> Graph:
    return Graph.create_empty_graph(n, AdjacencyList)

  @staticmethod
  def create_complete_graph(n: int) -> Graph:
    return Graph.create_complete_graph(n, AdjacencyList)

  @staticmethod
  def create_regular_graph(n: int, k: int) -> Graph:
    return Graph.create_regular_graph(n, k, AdjacencyList)


# Works only for simple graphs
class Walk:

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
