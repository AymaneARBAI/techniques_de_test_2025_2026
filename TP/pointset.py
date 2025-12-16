"""Fonctions utilitaires pour analyser et encoder le format binaire des PointSet."""

import struct
from collections.abc import Iterable

from TP.models import PointSet


def parse_pointset(binary_data: bytes) -> PointSet:
    """Analyser des données binaires et retourner un PointSet.

    Format attendu :
      - 4 octets little-endian (entier non signé) : nombre de points
      - pour chaque point : 4 octets float x, 4 octets float y (little-endian)
    """
    if not binary_data or len(binary_data) < 4:
        return PointSet(points=[])

    count = int.from_bytes(binary_data[:4], "little")
    pts = []
    offset = 4
    for _ in range(count):
        if len(binary_data) < offset + 8:
            break
        x = struct.unpack_from("<f", binary_data, offset)[0]
        y = struct.unpack_from("<f", binary_data, offset + 4)[0]
        pts.append((x, y))
        offset += 8
    return PointSet(points=pts)


def encode_pointset(points: Iterable[tuple[float, float]]) -> bytes:
    """Encode une séquence de points en représentation binaire."""
    out = len(list(points)).to_bytes(4, "little")
    for x, y in points:
        out += struct.pack("<f", float(x))
        out += struct.pack("<f", float(y))
    return out
