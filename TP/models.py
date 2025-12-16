"""Data models for point sets and triangle sets."""

from dataclasses import dataclass, field

Point = tuple[float, float]
Triangle = tuple[int, int, int]


@dataclass
class PointSet:
    """Représente un ensemble de points.

    The binary representation is:
    - 4 bytes little-endian unsigned int: number of points
    - for each point, 4 bytes little-endian float for X then 4 bytes for Y
    """

    points: list[Point] = field(default_factory=list)

    def to_bytes(self) -> bytes:
        """Encode this PointSet into the binary format described above."""
        import struct

        out = len(self.points).to_bytes(4, "little")
        for x, y in self.points:
            out += struct.pack("<f", float(x))
            out += struct.pack("<f", float(y))
        return out


@dataclass
class Triangles:
    """Représente un ensemble de triangles."""

    vertices: list[Point] = field(default_factory=list)
    triangles: list[Triangle] = field(default_factory=list)

    def __init__(
        self,
        vertices: list[Point] | None = None,
        sommets: list[Point] | None = None,
        triangles: list[Triangle] | None = None,
    ) -> None:
        """Construct a Triangles object accepting either `vertices` or `sommets`.

        Both `vertices` and `sommets` are accepted for compatibility with tests
        and previous names.
        """
        verts = vertices if vertices is not None else (sommets or [])
        self.vertices = list(verts)
        self.triangles = list(triangles or [])
        # compatibility alias (read/write)
        self.sommets = self.vertices

