from src.parser import Parser
from src.scheduler import Scheduler
from src.output import Output


if __name__ == "__main__":
    the_map = Parser().parse("maps/hard/01_maze_nightmare.txt")
    scheduler = Scheduler(the_map)
    turn = scheduler.simulator()
    output = Output(the_map, turn)
    output.write_down()
    output.visualization()
