#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   output.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/15 22:07:22 by junruan             #+#    #+#            #
#   Updated: 2026/06/16 23:05:49 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import matplotlib.pyplot as plt

from src.model import Map
from src.error import ParsingError


class Output:
    def __init__(self, the_map: Map, simulator: list[list[str]]) -> None:
        self.the_map = the_map
        self.simulator = simulator

    def write_down(self) -> None:
        for turn in self.simulator:
            move = " ".join(turn)
            print(move)

    def visualization(self) -> None:
        drone_position = {}
        if not self.the_map.nb_drones:
            raise ParsingError("missing 'nb_drones'")
        if not self.the_map.start:
            raise ParsingError("missing 'start'")
        for drone in range(1, (self.the_map.nb_drones + 1)):
            start_x = self.the_map.zones[self.the_map.start].x
            start_y = self.the_map.zones[self.the_map.start].y
            drone_position[f"D{drone}"] = (float(start_x), float(start_y))
        for turn in self.simulator:
            plt.clf()
            self._init_map()

            for move in turn:
                parts = move.split("-")
                drone_id = parts[0]
                x1 = self.the_map.zones[parts[1]].x
                y1 = self.the_map.zones[parts[1]].y
                if len(parts) == 3:
                    x2 = self.the_map.zones[parts[2]].x
                    y2 = self.the_map.zones[parts[2]].y
                    drone_position[drone_id] = (((x1+x2)/2), ((y1+y2)/2))
                if len(parts) == 2:
                    drone_position[drone_id] = (x1, y1)

            for drone_id, pos in drone_position.items():
                plt.scatter(pos[0], pos[1], color="grey", s=200, marker="*")
                plt.annotate(
                    drone_id,
                    (pos[0], pos[1]),
                    textcoords="offset points",
                    xytext=(-10, 20),
                    fontsize=8
                )
            plt.pause(2)
        plt.show()

    def _init_map(self) -> None:
        for zone in self.the_map.zones:
            if not self.the_map.zones[zone].color:
                self.the_map.zones[zone].color = "black"
            try:
                plt.scatter(
                    self.the_map.zones[zone].x,
                    self.the_map.zones[zone].y,
                    color=self.the_map.zones[zone].color,
                    s=200,
                    marker="s"
                )
            except ValueError:
                plt.scatter(
                    self.the_map.zones[zone].x,
                    self.the_map.zones[zone].y,
                    color="black",
                    s=100
                )
            plt.annotate(
                zone,
                (self.the_map.zones[zone].x, self.the_map.zones[zone].y),
                textcoords="offset points",
                xytext=(-10, 10),
                fontsize=6
            )
        for _, conn in self.the_map.connections.items():
            x1 = self.the_map.zones[conn.zone_a].x
            y1 = self.the_map.zones[conn.zone_a].y
            x2 = self.the_map.zones[conn.zone_b].x
            y2 = self.the_map.zones[conn.zone_b].y
            plt.plot([x1, x2], [y1, y2], color="grey", linestyle=":")
