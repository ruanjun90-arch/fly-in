#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/17 22:27:06 by junruan             #+#    #+#            #
#   Updated: 2026/06/17 22:38:50 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys

from src.error import ParsingError
from src.output import Output
from src.parser import Parser
from src.scheduler import Scheduler


AVAILABLE_MAPS = {
    "1": "maps/easy/01_linear_path.txt",
    "2": "maps/easy/02_simple_fork.txt",
    "3": "maps/easy/03_basic_capacity.txt",
    "4": "maps/medium/01_dead_end_trap.txt",
    "5": "maps/medium/02_circular_loop.txt",
    "6": "maps/medium/03_priority_puzzle.txt",
    "7": "maps/hard/01_maze_nightmare.txt",
    "8": "maps/hard/02_capacity_hell.txt",
    "9": "maps/hard/03_ultimate_challenge.txt",
    "10": "maps/challenger/01_the_impossible_dream.txt",
}


def choose_map_from_menu() -> str:
    """Display a menu and return the selected map path."""
    print("Choose a map:")
    print("1. Easy - Linear path")
    print("2. Easy - Simple fork")
    print("3. Easy - Basic capacity")
    print("4. Medium - Dead end trap")
    print("5. Medium - Circular loop")
    print("6. Medium - Priority puzzle")
    print("7. Hard - Maze nightmare")
    print("8. Hard - Capacity hell")
    print("9. Hard - Ultimate challenge")
    print("10. Challenger - Impossible dream")

    choice = input("Map number: ").strip()

    if choice not in AVAILABLE_MAPS:
        raise ParsingError(f"invalid map choice: {choice}")

    return AVAILABLE_MAPS[choice]


def run_simulation(map_file: str, show_visual: bool) -> None:
    """Run parser, scheduler, and output for one map file."""
    the_map = Parser().parse(map_file)
    scheduler = Scheduler(the_map)
    turns = scheduler.simulator()
    output = Output(the_map, turns)

    output.write_down()

    if show_visual:
        output.visualization()


def main() -> None:
    """Run the Fly-in simulation."""
    args = sys.argv[1:]
    show_visual = False

    if "--visual" in args:
        show_visual = True
        args.remove("--visual")

    try:
        if "--menu" in args:
            args.remove("--menu")

            if args:
                print("Usage: python3 -m src [--visual] --menu")
                return

            map_file = choose_map_from_menu()
        else:
            if len(args) != 1:
                print("Usage: python3 -m src [--visual] <map_file>")
                print("       python3 -m src [--visual] --menu")
                return

            map_file = args[0]

        run_simulation(map_file, show_visual)

    except ParsingError as error:
        print(f"Error: {error}")
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
