from src.error import ParsingError
from src.model import ZoneType


def split_metadata(
    content: str,
    line_no: int,
) -> tuple[str, dict[str, str]]:
    """Split main content and metadata block."""
    if "[" not in content:
        return content.strip(), {}

    before_metadata, raw_metadata = content.split("[", 1)

    if not raw_metadata.endswith("]"):
        raise ParsingError(
            f"Line {line_no}: metadata block must end with ']'"
        )

    metadata_content = raw_metadata[:-1].strip()
    metadata = parse_metadata_block(metadata_content, line_no)

    return before_metadata.strip(), metadata


def parse_metadata_block(
    metadata_content: str,
    line_no: int,
) -> dict[str, str]:
    """Parse metadata key-value pairs."""
    metadata: dict[str, str] = {}

    if not metadata_content:
        return metadata

    for item in metadata_content.split():
        if "=" not in item:
            raise ParsingError(
                f"Line {line_no}: invalid metadata item '{item}'"
            )

        key, value = item.split("=", 1)

        if not key or not value:
            raise ParsingError(
                f"Line {line_no}: invalid metadata item '{item}'"
            )

        metadata[key] = value

    return metadata
