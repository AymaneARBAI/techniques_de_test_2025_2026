"""Client helper utilities for PointSet manager interactions."""

Point = tuple[float, float]


def decode_pointset(data: bytes) -> list[Point]:
    """Decode a PointSet binary payload from the client."""
    raise NotImplementedError


def store_pointset(points: list[Point]) -> str:
    """Store a decoded PointSet and return its PointSetID."""
    raise NotImplementedError


def register_pointset(data: bytes) -> str:
    """High-level function to handle POST /pointset.

    Steps:
    1. Decode the received binary data.
    2. Store the PointSet.
    3. Return the PointSetID to the client.
    """
    raise NotImplementedError
