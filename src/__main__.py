from src.parser import Parser
from src.pathfinding import PathFinder
from src.scheduler import Scheduler


if __name__ == "__main__":
    the_map = Parser().parse("maps/challenger/01_the_impossible_dream.txt")
    p_d = PathFinder(the_map).dijkstra()
    cost_d = PathFinder(the_map).compute_path_cost(p_d)
    scheduler = Scheduler(the_map)
    turn = scheduler.simulator()
    print(turn)
