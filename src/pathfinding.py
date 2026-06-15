#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   pathfinding.py                                       :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/14 19:48:47 by junruan             #+#    #+#            #
#   Updated: 2026/06/14 19:48:48 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from collections import deque
import heapq

from src.model import Map, ZoneType


class PathFinder:
    """Find paths on a map using BFS or Dijkstra."""

    def __init__(self, the_map: Map) -> None:
        """Store the map used by the pathfinding algorithms.

        Args:
            the_map: Parsed map used for pathfinding.
        """
        self.the_map = the_map

    def bfs(self) -> list[str]:
        """Return a shortest path in number of steps.

        This ignores zone weights and only avoids blocked zones.

        Returns:
            A path from start to end as a list of zone names.
        """
        if self.the_map.start is None or self.the_map.end is None:
            raise ValueError("map has no start or end")
        zone_to_discov = deque([self.the_map.start])
        came_from: dict[str, str | None] = {self.the_map.start: None}
        path = []
        while zone_to_discov:
            zone_current = zone_to_discov.popleft()
            if zone_current == self.the_map.end:
                break
            else:
                for neighbor in self.the_map.adjacency[zone_current]:
                    if neighbor not in came_from:
                        if self.the_map.zones[neighbor].zone_type == ZoneType.BLOCKED:  # noqa: E501
                            continue
                        came_from[neighbor] = zone_current
                        zone_to_discov.append(neighbor)
        if self.the_map.end not in came_from:
            raise ValueError("no path found")
        current: str | None = self.the_map.end
        while current is not None:
            path.append(current)
            current = came_from[current]
        return path[::-1]

    def dijkstra(self) -> list[str]:
        """Return the lowest-cost path using zone entry costs.

        Returns:
            A path from start to end as a list of zone names.
        """
        if self.the_map.start is None or self.the_map.end is None:
            raise ValueError("map has no start or end")
        heap: list[tuple[int, str]] = [(0, self.the_map.start)]
        came_from: dict[str, str | None] = {self.the_map.start: None}
        cost_so_far: dict[str, int] = {self.the_map.start: 0}
        visited: set[str] = set()
        path = []
        while heap:
            cost, zone_current = heapq.heappop(heap)
            if zone_current in visited:
                continue
            visited.add(zone_current)
            if zone_current == self.the_map.end:
                break
            else:
                for neighbor in self.the_map.adjacency[zone_current]:
                    if self.the_map.zones[neighbor].zone_type == ZoneType.BLOCKED:  # noqa: E501
                        continue
                    if self.the_map.zones[neighbor].zone_type == ZoneType.NORMAL:  # noqa: E501
                        step_cost = 1
                    elif self.the_map.zones[neighbor].zone_type == ZoneType.RESTRICTED:  # noqa: E501
                        step_cost = 2
                    elif self.the_map.zones[neighbor].zone_type == ZoneType.PRIORITY:  # noqa: E501
                        step_cost = 1
                    new_cost = step_cost + cost_so_far[zone_current]
                    if (neighbor not in cost_so_far
                            or new_cost < cost_so_far[neighbor]):
                        cost_so_far[neighbor] = new_cost
                        came_from[neighbor] = zone_current
                        heapq.heappush(heap, (new_cost, neighbor))
        if self.the_map.end not in came_from:
            raise ValueError("no path found")
        current: str | None = self.the_map.end
        while current is not None:
            path.append(current)
            current = came_from[current]
        return path[::-1]

    def compute_path_cost(self, path: list[str]) -> int:
        """Compute the total traversal cost of a path.

        Args:
            path: A path produced by ``bfs`` or ``dijkstra``.

        Returns:
            The total traversal cost for the path.

        Raises:
            ValueError: If the path contains a blocked zone.
        """
        total = 0
        for zone_name in path[1:]:
            zone_type = self.the_map.zones[zone_name].zone_type
            if zone_type == ZoneType.BLOCKED:
                raise ValueError(f"path contains blocked zone: {zone_name}")
            if zone_type == ZoneType.RESTRICTED:
                total += 2
            else:
                total += 1
        return total
