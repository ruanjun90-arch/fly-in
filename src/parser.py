#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parser.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/08 23:50:48 by junruan             #+#    #+#            #
#   Updated: 2026/06/09 19:59:58 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from pathlib import Path

from src.error import ParsingError
from src.model import Map, Zone
from src.parsing_utils import (
    parse_metadata_block,
    parse_positive_int,
    parse_zone_type,
    split_metadata,
)


class Parser:
    """Parse a Fly-in map file into a graph."""

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.map = Map()
        self.nb_drones: int | None = None

    def parse(self) -> tuple[int, Map]:
        """Parse the map file and return drone count with map."""
        if not self.file_path.exists():
            raise ParsingError(f"File not found: {self.file_path}")

        with self.file_path.open("r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                self._parse_line(line, line_no)

        self._validate_result()

        if self.nb_drones is None:
            raise ParsingError("Missing nb_drones declaration")

        return self.nb_drones, self.map

    def _parse_zone(
        self,
        content: str,
        line_no: int,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        """Parse a zone line and add it to the map."""
        main_content, metadata = split_metadata(content, line_no)
        parts = main_content.split()

        if len(parts) != 3:
            raise ParsingError(
                f"Line {line_no}: zone must have name, x and y"
            )

        name = parts[0]

        if "-" in name:
            raise ParsingError(
                f"Line {line_no}: zone name cannot contain '-'"
            )

        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError as error:
            raise ParsingError(
                f"Line {line_no}: zone coordinates must be integers"
            ) from error

        zone = Zone(
            name=name,
            x=x,
            y=y,
            zone_type=parse_zone_type(metadata.get("zone"), line_no),
            color=metadata.get("color"),
            max_drones=parse_positive_int(
                metadata.get("max_drones"),
                "max_drones",
                1,
                line_no,
            ),
        )

        try:
            self.map.add_zone(zone)
        except ValueError as error:
            raise ParsingError(f"Line {line_no}: {error}") from error

        if is_start:
            if self.map.start is not None:
                raise ParsingError(f"Line {line_no}: start_hub already defined")
            self.map.start = name

        if is_end:
            if self.map.end is not None:
                raise ParsingError(f"Line {line_no}: end_hub already defined")
            self.map.end = name
