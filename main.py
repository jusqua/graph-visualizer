from lib import AdjacencyList


def main():
  # elements = [(1, 2), (2, 1), (1, 2)]
  elements = [(1, -2), (-1, 2), (-1, -2), (1, -3)]
  print(AdjacencyList.is_2satisfiable(elements))


if __name__ == "__main__":
  main()
