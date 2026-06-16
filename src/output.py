#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   output.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/15 22:07:22 by junruan             #+#    #+#            #
#   Updated: 2026/06/16 14:14:48 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import matplotlib.pyplot as plt

from src.model import Map


class Output:
    def __init__(self, the_map: Map, simulator: list[list[str]]) -> None:
        self.the_map = the_map
        self.simulator = simulator

    def write_down(self) -> None:
        for turn in self.simulator:
            move = " ".join(turn)
            print(move)

    def visualization(self) -> None:
        for zone in self.the_map.zones:
            plt.scatter(
                self.the_map.zones[zone].x,
                self.the_map.zones[zone].y,
                color=self.the_map.zones[zone].color,
                s=100
            )
            plt.annotate(
                zone,
                (self.the_map.zones[zone].x, self.the_map.zones[zone].y),
                textcoords="offset points",
                xytext=(-10, 10),
                fontsize=8
            )
        for _, conn in self.the_map.connections.items():
            x1 = self.the_map.zones[conn.zone_a].x
            y1 = self.the_map.zones[conn.zone_a].y
            x2 = self.the_map.zones[conn.zone_b].x
            y2 = self.the_map.zones[conn.zone_b].y
            plt.plot([x1, x2], [y1, y2], color="grey")
        plt.show()
