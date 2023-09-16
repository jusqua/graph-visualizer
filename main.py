from lib import AdjacencyList


def main():
  g = AdjacencyList.create_empty_graph(7, directed=True)
  
  for e in [(0, 1), (1, 0), (2, 0), (2, 1), (2, 3), (3, 2), (4, 1), (4, 3), (4, 5), (5, 3), (5, 6), (6, 4)]:
    g.create_edge(*e)

  for i, list in enumerate(g.content):
    print(f"Lista de {g.vertices[i].label}: ", end=" ")
    for v in list:
      print(v.label, end=" ")
    print()
  print()

  print(g.strong_connected_components())
    
if __name__ == "__main__":
  main()
