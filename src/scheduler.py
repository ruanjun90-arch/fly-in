#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   scheduler.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/14 19:48:55 by junruan             #+#    #+#            #
#   Updated: 2026/06/15 19:06:03 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from collections import Counter

from src.model import Map, ZoneType
from src.error import ParsingError
from src.pathfinding import PathFinder


class Scheduler:
    def __init__(self, the_map: Map) -> None:
        self.the_map = the_map
        self.pathfinder = PathFinder(the_map)
        if self.the_map.nb_drones is None:
            raise ParsingError("missing 'nb_drones'")
        if self.the_map.start is None:
            raise ParsingError("missing 'start'")
        self.drone_position: dict[int, str] = {}
        self.drone_paths: dict[int, list[str]] = {}
        self.drone_step: dict[int, int] = {}

        path = self.pathfinder.dijkstra()
        for drone in range(1, (self.the_map.nb_drones + 1)):
            self.drone_position[drone] = self.the_map.start
            self.drone_paths[drone] = path
            self.drone_step[drone] = 0

    def simulator(self) -> list[list[str]]:
        turn = []
        in_transit: dict[int, str] = {}
        while not all(
            position == self.the_map.end
            for position in self.drone_position.values()
        ):
            turn_moves = []
            link_usage: dict[frozenset[str], int] = {}
            drone_in_zone = Counter(self.drone_position.values())
            landed = set()

            for drone_id in list(in_transit.keys()):
                destination = in_transit[drone_id]
                self.drone_position[drone_id] = destination
                drone_in_zone[destination] += 1
                turn_moves.append(f"D{drone_id}-{destination}")
                del in_transit[drone_id]
                landed.add(drone_id)

            for drone_id, position in self.drone_position.items():
                if position == self.the_map.end:
                    continue
                if drone_id in in_transit:
                    continue
                if drone_id in landed:
                    continue
                next_zone = self.drone_paths[drone_id][(
                    self.drone_step[drone_id]
                    ) + 1]
                zone_limitation = self.the_map.zones[next_zone].max_drones
                conn_key = frozenset({position, next_zone})
                connection = self.the_map.connections[conn_key]
                conn_limit = connection.max_link_capacity
                if (next_zone == self.the_map.end
                        or drone_in_zone[next_zone] < zone_limitation
                        and link_usage.get(conn_key, 0) < conn_limit):
                    link_usage[conn_key] = link_usage.get(conn_key, 0) + 1
                    zone_type = self.the_map.zones[next_zone].zone_type
                    if zone_type == ZoneType.RESTRICTED:
                        in_transit[drone_id] = next_zone
                        self.drone_step[drone_id] += 1
                        turn_moves.append(
                            f"D{drone_id}-{position}-{next_zone}"
                        )
                    else:
                        drone_in_zone[next_zone] += 1
                        drone_in_zone[self.drone_position[drone_id]] -= 1
                        self.drone_position[drone_id] = next_zone
                        self.drone_step[drone_id] += 1
                        turn_moves.append(
                            f"D{drone_id}-{next_zone}"
                        )
            if not turn_moves:
                break
            turn.append(turn_moves)
        return turn
