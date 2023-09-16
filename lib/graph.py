from __future__ import annotations
from typing import Optional
from copy import deepcopy
from lib.edge import Edge
from lib.vertex import Vertex


class Graph:

  def __init__(self, *, is_digraph: bool = False):
    self.vertices: list[Vertex] = []
    self.edges: list[Edge] = []
    self.is_digraph = is_digraph

  def append_vertex(self, label: str):
    index = len(self.vertices)
    self.vertices.append(Vertex(index, label))

  def create_edge(self, ix: int, iy: int, label: Optional[str] = None):
    vx = self.vertices[ix]
    vy = self.vertices[iy]

    vx.degree += 1
    vy.degree += 1

    self.edges.append(Edge(vx, vy, label, is_digraph=self.is_digraph))

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

  def validate_edges(self, edges: list[tuple[int, int, Optional[str]]]) -> bool:
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
  def create_empty_graph(n: int, *, graph_type: type[Graph], is_digraph: bool = False) -> Graph:
    g = graph_type(is_digraph=is_digraph)

    for i in range(n):
      g.append_vertex(f"v{i + 1}")

    return g

  @staticmethod
  def create_complete_graph(n: int, *, graph_type: type[Graph]) -> Graph:
    kn = Graph.create_empty_graph(n, graph_type)

    for i in range(n):
      for j in range(i + 1, n):
        kn.create_edge(i, j)

    return kn

  @staticmethod
  def create_regular_graph(n: int, k: int, *, graph_type: type[Graph]) -> Graph:
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
