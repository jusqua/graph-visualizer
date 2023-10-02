from lib import AdjacencyList


def CNF_to_str(elements: list[tuple[int, int]]) -> str:
  cnf = ""
  for u, v in elements:
    cnf += f"({'¬' if u < 0 else ''}x{abs(u)} ∨ {'¬' if v < 0 else ''}x{abs(v)}) ∧ "
  cnf = cnf[:-3]

  return cnf
  

def main():
  # elements = [(1, -2), (-1, 2), (-1, -2), (1, -3)] # True
  # elements = [(1, 2), (-1, 2), (1, -2), (-1, -2)] # False
  elements = [(1, 2), (-2, 3), (-1, -2), (3, 4), (-3, 5), (-4, -5), (-3, 4)] # True
  print(CNF_to_str(elements))
  print(AdjacencyList.is_2satisfiable(elements))

if __name__ == "__main__":
  main()
