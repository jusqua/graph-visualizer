from lib.graph import AdjacencyList


def main():
  g = AdjacencyList(is_digraph=True)
  for v in ["0", "1", "2", "3", "4", "5", "6"]:
    g.append_vertex(v)
  for e in [(0, 1), (1, 0), (2, 0), (2, 1), (2, 3), (3, 2), (4, 1), (4, 3), (4, 5), (5, 3), (5, 6), (6, 4)]:
  # for e in [(0, 1), (1, 2), (1, 4), (1, 6), (2, 3), (3, 2), (3, 4), (3, 5), (4, 5), (5, 4), (6, 0), (6, 2)]:
  # for e in [(0, 1), (1, 0), (2, 0), (2, 3), (3, 4), (4, 0), (4, 2), (4, 5), (5, 1)]:
    g.create_edge(*e)

  for list in g.content:
    print(f"Lista de {list[0].label}: ", end=" ")
    for v in list[1:]:
      print(v.label, end=" ")
    print()
  print()

  print(g.strong_connected_components())
    
if __name__ == "__main__":
  main()
