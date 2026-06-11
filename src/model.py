#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   model.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/08 11:42:21 by junruan             #+#    #+#            #
#   Updated: 2026/06/11 11:20:53 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from dataclasses import dataclass, field
from enum import Enum


class ZoneType(Enum):
    """Available zone types in the map."""
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass
class Zone:
    """A zone in the drone network."""
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1


@dataclass(frozen=True)
class Connection:
    """A bidirectional connection between two zones."""
    zone_a: str
    zone_b: str
    max_link_capacity: int = 1

    def key(self) -> frozenset[str]:
        """Return an order-independent identifier for this connection."""
        return frozenset({self.zone_a, self.zone_b})


@dataclass
class Map:
    """A network of zones connected by bidirectional links."""
    start: str | None = None
    end: str | None = None
    nb_drones: int | None = None
    zones: dict[str, Zone] = field(default_factory=dict)
    adjacency: dict[str, list[str]] = field(default_factory=dict)
    connections: dict[frozenset[str], Connection] = field(default_factory=dict)
