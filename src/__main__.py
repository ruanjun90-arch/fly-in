from src.parser import Parser
from src.pathfinding import PathFinder


def main() -> None:
    the_map = Parser().parse("maps/medium/03_priority_puzzle.txt")
    p_d = PathFinder(the_map).dijkstra()
    cost_d = PathFinder(the_map).compute_path_cost(p_d)
    p_b = PathFinder(the_map).bfs()
    cost_b = PathFinder(the_map).compute_path_cost(p_b)
    print(f"dijkstra method: {p_d}")
    print(f"total step cost by dijkstra: {cost_d}")
    print(f"bfs method: {p_b}")
    print(f"total step cost by bfs: {cost_b}")


if __name__ == "__main__":
    main()
