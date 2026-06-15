#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   output.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/15 22:07:22 by junruan             #+#    #+#            #
#   Updated: 2026/06/15 22:53:16 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

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
        pass
