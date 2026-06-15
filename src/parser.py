#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parser.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/14 19:48:39 by junruan             #+#    #+#            #
#   Updated: 2026/06/14 19:48:40 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from src.error import ParsingError
from src.model import Map, Zone, Connection, ZoneType


class Parser:
    """Parse Fly-in map files into ``Map`` objects."""

    def __init__(self) -> None:
        """Initialize an empty parser state."""
        self.map = Map()

    def _read_lines(self, file_path: str) -> list[tuple[int, str]]:
        """Read and normalize meaningful lines from a file.

        Args:
            file_path: Path to the input file.

        Returns:
            A list of ``(line_number, content)`` tuples for non-empty,
            non-comment lines.

        Raises:
            ParsingError: If the path is empty or the file does not exist.
        """
        if not file_path:
            raise ParsingError("file path is empty")
        try:
            with open(file_path) as file:
                lines = []
                for line_nb, line in enumerate(file, start=1):
                    clean_line = line.strip()
                    if not clean_line:
                        continue
                    elif clean_line.startswith("#"):
                        continue
                    else:
                        lines.append((line_nb, clean_line))
                return lines
        except FileNotFoundError:
            raise ParsingError(f"no file {file_path} detected")

    def parse(self, file_path: str) -> Map:
        """Parse a map file into a ``Map`` instance.

        Args:
            file_path: Path to the map definition file.

        Returns:
            The parsed map.

        Raises:
            ParsingError: If the file content is invalid or incomplete.
        """
        lines = self._read_lines(file_path)

        if not lines:
            raise ParsingError("the file is empty")

        first_line_nb, first_line = lines[0]
        if first_line.split(":", 1)[0].strip() != "nb_drones":
            raise ParsingError(
                f"line {first_line_nb}: first line must be 'nb_drones'"
            )
        else:
            self._parse_nb_drones(first_line, first_line_nb)

        for line_nb, line in lines[1:]:
            if ":" in line:
                prefix = line.split(":", 1)[0].strip()
                if prefix in ("start_hub", "end_hub", "hub"):
                    self._parse_zones(line, line_nb)
                elif prefix == "connection":
                    self._parse_connection(line, line_nb)
                else:
                    raise ParsingError(
                        f"line {line_nb}: unknown prefix '{prefix}'"
                    )
            else:
                raise ParsingError(f"line {line_nb}: missing ':' separator")
        if self.map.start is None:
            raise ParsingError("missing 'start'")
        if self.map.end is None:
            raise ParsingError("missing 'end'")
        return self.map

    def _parse_nb_drones(self, line: str, line_nb: int) -> None:
        """Parse the ``nb_drones`` declaration.

        Args:
            line: The raw ``nb_drones: ...`` line.
            line_nb: 1-based line number used in error messages.

        Raises:
            ParsingError: If the value is not a positive integer.
        """
        _, content = line.split(":", 1)
        try:
            number = int(content.strip().strip('"'))
        except ValueError:
            raise ParsingError(
                f"line {line_nb}: '{content.strip()}' is not a valid integer"
            )
        if number <= 0:
            raise ParsingError(
                f"line {line_nb}: nb_drones must be positive, got {number}"
            )
        self.map.nb_drones = number

    def _parse_zones(self, line: str, line_nb: int) -> None:
        """Parse a zone declaration and store it in the map.

        Args:
            line: The raw zone declaration line.
            line_nb: 1-based line number used in error messages.

        Raises:
            ParsingError: If the zone definition or metadata is invalid.
        """
        prefix, content = line.split(":", 1)
        meta_dict: dict[str, str] = {}
        if "[" in line:
            if "]" not in line:
                raise ParsingError(
                    f"line {line_nb}: "
                    "metadata block is not syntactically valid"
                )
            else:
                content, meta = content.split("[", 1)
                meta = meta.rstrip("]")
                for pair in meta.split():
                    try:
                        key, value = pair.split("=", 1)
                    except ValueError:
                        raise ParsingError(
                            f"line {line_nb}: invalid metadata '{pair}'"
                        )
                    meta_dict[key] = value
        try:
            name_str, x, y = content.strip().split()
        except ValueError:
            raise ParsingError(
                f"line {line_nb}: expected '<name> <x> <y>', "
                f"got '{content.strip()}'"
            )
        if "-" in name_str:
            raise ParsingError(
                f"line {line_nb}: names cannot use '-' or ' '"
            )
        try:
            x_int = int(x)
            y_int = int(y)
        except ValueError:
            raise ParsingError(
                f"line {line_nb}: coordinates must be integers, got '{x} {y}'"
            )
        try:
            zone_type = ZoneType(meta_dict.get("zone", "normal"))
        except ValueError:
            raise ParsingError(
                f"line {line_nb}: invalid zone type '{meta_dict.get('zone')}'"
            )
        try:
            max_drones = int(meta_dict.get("max_drones", "1"))

        except ValueError:
            raise ParsingError(
                f"line {line_nb}: max_drones must be an integer"
            )

        if max_drones <= 0:
            raise ParsingError(
                f"line {line_nb}: max_drones must be a positive integer"
            )

        zone = Zone(
            name_str,
            x_int,
            y_int,
            zone_type=zone_type,
            color=meta_dict.get("color"),
            max_drones=max_drones,
        )
        if name_str in self.map.zones:
            raise ParsingError(
                f"line {line_nb}: duplicated zone name {name_str}"
            )
        self.map.zones[name_str] = zone
        if prefix.strip() == "start_hub":
            if self.map.start is not None:
                raise ParsingError(f"line {line_nb}: duplicated 'start'")
            self.map.start = name_str
        elif prefix.strip() == "end_hub":
            if self.map.end is not None:
                raise ParsingError(f"line {line_nb}: duplicated 'end'")
            self.map.end = name_str

    def _parse_connection(self, line: str, line_nb: int) -> None:
        """Parse a connection declaration and store it in the map.

        Args:
            line: The raw connection declaration line.
            line_nb: 1-based line number used in error messages.

        Raises:
            ParsingError: If the connection definition or metadata is invalid.
        """
        _, content = line.split(":", 1)
        max_link_capacity = 1
        if "[" in line:
            if "]" not in line:
                raise ParsingError(
                    f"line {line_nb}: "
                    "metadata block is not syntactically valid"
                )
            else:
                content, meta = content.split("[", 1)
                meta = meta.rstrip("]")
            try:
                _, value = meta.strip().split("=", 1)
                max_link_capacity = int(value)
            except ValueError:
                raise ParsingError(
                    f"line {line_nb}: invalid connection metadata '{meta}'"
                )
            if max_link_capacity <= 0:
                raise ParsingError(
                    f"line {line_nb}: "
                    "max_link_capacity must be a positive integer"
                )
        try:
            zone_a, zone_b = content.strip().split("-", 1)
        except ValueError:
            raise ParsingError(
                f"line {line_nb}: connection must be '<zone1>-<zone2>'"
            )
        if zone_a not in self.map.zones:
            raise ParsingError(f"line {line_nb}: zone {zone_a} is not defined")
        if zone_b not in self.map.zones:
            raise ParsingError(f"line {line_nb}: zone {zone_b} is not defined")
        conn = Connection(zone_a, zone_b, max_link_capacity)
        if conn.key() in self.map.connections:
            raise ParsingError(f"line {line_nb}: duplicated connection")
        self.map.connections[conn.key()] = conn
        self.map.adjacency.setdefault(zone_a, []).append(zone_b)
        self.map.adjacency.setdefault(zone_b, []).append(zone_a)
