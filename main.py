from lib.graph import AdjacencyList, Walk


def main():
  g = AdjacencyList()
  for v in ["u", "v", "w", "x", "y"]:
    g.append_vertex(v)
  for e in [(0, 1, "a"), (1, 2, "b"), (2, 3, "c"), (3, 4, "d"), (0, 4, "e"), (1, 4, "f"), (2, 4, "h")]:
    g.create_edge(*e)
    
  h = AdjacencyList()
  for v in ["u", "v", "w", "x", "y"]:
    h.append_vertex(v)
  for e in [(0, 1, "a"), (1, 2, "b"), (1, 3, "c"), (3, 4, "d")]:
    h.create_edge(*e)
    
  j = AdjacencyList()
  for v in ["u", "v", "w", "x", "y", "z"]:
    j.append_vertex(v)
  for e in [(0, 1, "a"), (1, 2, "b"), (2, 0, "c"), (3, 4, "d"), (4, 5, "e"), (5, 3, "f")]:
    j.create_edge(*e)
  
  k = AdjacencyList()
  for v in ["u", "v", "w", "x", "y"]:
    k.append_vertex(v)
  for e in [(0, 1, "a"), (1, 2, "b"), (2, 0, "c"), (3, 4, "d")]:
    k.create_edge(*e)
    
  walk = Walk(g, [0, 1, 2, 3, 4, 0, 4])
  print(walk.get_primitive())
  print("\n")

  print(walk.get_primitive(reverse=True))
  print("\n")

  section = walk.section(2, 5)
  print(section.get_primitive())
  print("\n")

  paths = g.get_all_paths_between(0, 1)
  for path in paths:
    print(path.get_primitive())
  print("\n")

  walk = g.find_cycle() 
  print(walk.get_primitive() if walk else "Acyclic graph")  
  print("\n")
  
  walk = g.restricted_find_cycle() 
  print(walk.get_primitive() if walk else "Acyclic graph")  
  print("\n")
  
  print(g.get_components())
  print(k.get_components())
  print("\n")
  
  print(g.contains_circuit())
  print(h.contains_circuit())
  print(j.contains_circuit())
  print(k.contains_circuit())
  print("\n")

  print(g.is_connected())
  print(h.is_connected())
  print(j.is_connected())
  print(k.is_connected())
  print("\n")

  circuit = Walk(g, [0, 4, 2, 3, 4, 1, 0])
  cycle = g.get_cycle_from_circuit(circuit, (1, 2))
  print(cycle.get_primitive())
  print("\n")
    
  walk = Walk(g, [2, 3, 4, 0, 4, 3, 4, 1, 2])
  path = walk.get_path()
  print(path.get_primitive())
  print("\n")
  
  g = AdjacencyList()
  for v in ["u", "v", "w", "x", "y"]:
    g.append_vertex(v)
  for e in [(0, 1, "a"), (1, 2, "b"), (2, 3, "c"), (3, 4, "d"), (0, 4, "e"), (1, 4, "f"), (1, 4, "g"), (2, 4, "h")]:
    g.create_edge(*e)
  print("Graph G:")
  print(g)

  x1 = [0, 1, 3, 4]
  ig = g.create_induced_subgraph(x1)
  print("X1:", x1)
  print("Induced Subgraph of G:")
  print(ig)

  x2 = [0, 2]
  g_x2 = g.subtract_vertices(x2)
  print("X2:", x2)
  print("Subgraph G-X2:")
  print(g_x2)

  e1 = [(0, 1, "a"), (2, 3, "c"), (0, 4, "e"), (1, 4, "g")]
  eig = g.create_edge_induced_subgraph(e1)
  print("E1:", e1)
  print("Edge Induced Subgraph of G:")
  print(eig)

  e2 = [(0, 1, "a"), (1, 2, "b"), (1, 4, "f")]
  g_e2 = g.subtract_edges(e2)
  print("E2:", e2)
  print("Subgraph G-E2:")
  print(g_e2)
  
  g = AdjacencyList()
  for i in range(8):
    label = str(chr(i + 97))
    g.append_vertex(label)

  g.create_edge(0, 1)
  g.create_edge(0, 2)
  g.create_edge(0, 4)
  g.create_edge(0, 5)
  g.create_edge(1, 3)
  g.create_edge(1, 4)
  g.create_edge(2, 5)
  g.create_edge(2, 6)
  g.create_edge(2, 7)
  g.create_edge(5, 6)
  g.create_edge(5, 7)
  g.create_edge(6, 7)

  g.dfs()

  tree_edges = [tuple(e) for e in g.tree_edges]
  back_edges = [tuple(e) for e in g.back_edges]

  print(f"Tree edges:\n {tree_edges}\n")
  print(f"Back edges:\n {back_edges}\n")

  print("Depth")
  for v in g.vertices:
    print(f"Label: {v.label} | Entry: {v.entry_depth} | Exit: {v.exit_depth}")

  print(AdjacencyList.create_complete_graph(5))

  print(AdjacencyList.create_regular_graph(7, 4))

  g = AdjacencyList.create_empty_graph(4)
  g.create_edge(0, 1)
  g.create_edge(0, 3)
  g.create_edge(1, 2)
  g.create_edge(2, 3)

  print(g)
  
  division1 = ([0, 2], [1, 3])
  print(g.is_bipartite(*division1))
  
  division2 = ([0, 1], [2, 3])
  print(g.is_bipartite(*division2))


if __name__ == "__main__":
  main()
