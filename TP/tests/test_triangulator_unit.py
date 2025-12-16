"""Tests unitaires pour le Triangulator."""

import struct

from TP.models import PointSet, Triangles
from TP.Triangulator import Triangulator


def test_triangulate_small_pointset():
    """Vérifie que triangulate renvoie aucun triangle pour 0, 1 ou 2 points."""
    triangulator = Triangulator()

    pointset1 = PointSet(points=[])
    pointset2 = PointSet(points=[(0, 0)])
    pointset3 = PointSet(points=[(0, 0), (1, 0)])

    triangulator.get_PointSet = lambda: {"id1": pointset1}
    assert triangulator.triangulate("id1").triangles == []

    triangulator.get_PointSet = lambda: {"id2": pointset2}
    assert triangulator.triangulate("id2").triangles == []

    triangulator.get_PointSet = lambda: {"id3": pointset3}
    assert triangulator.triangulate("id3").triangles == []


def test_triangulator_three_points_non_aligned():
    """Vérifie que 3 points non alignés produisent exactement 1 triangle."""
    triangulator = Triangulator()
    triangulator.get_PointSet = lambda: {"id": PointSet(points=[(0,0), (1,0), (0,1)])}

    res = triangulator.triangulate("id")
    assert len(res.triangles) == 1


def test_triangulator_three_points_aligned():
    """Vérifie que 3 points alignés ne produisent aucun triangle."""
    tri = Triangulator()
    tri.get_PointSet = lambda: {"id": PointSet(points=[(0,0),(1,0),(2,0)])}

    res = tri.triangulate("id")
    assert res.triangles == []


def test_triangulator_invalid_values():
    """Vérifie que des valeurs impossibles ne produisent aucun triangle."""
    tri = Triangulator()
    tri.get_PointSet = lambda: {"id": PointSet(points=[(0,0), (1,0), (None, 0)])}

    res = tri.triangulate("id")
    assert res.triangles == []

def test_triangulator_duplicated_points():
    """Vérifie que des points dupliqués empêchent la création d’un triangle."""
    tri = Triangulator()
    tri.get_PointSet = lambda: {"id": PointSet(points=[(0,0),(1,0),(1,0)])}

    res = tri.triangulate("id")
    assert res.triangles == []


def test_triangulator_four_points_square():
    """Vérifie que 4 points forment bien 2 triangles."""
    tri = Triangulator()
    tri.get_PointSet = lambda: { "id": PointSet(points=[(0,0), (1,0), (1,1), (0,1)])}

    res = tri.triangulate("id")
    assert len(res.triangles) == 2



def test_triangulator_returns_triangles_object():
    """Vérifie que triangulate retourne bien un objet Triangles."""
    tri = Triangulator()

    def _get_pointset(point_set_id):
        return {"id": PointSet(points=[(0, 0), (1, 0), (0, 1)])}[point_set_id]

    tri.get_PointSet = _get_pointset

    res = tri.triangulate("id")
    assert isinstance(res, Triangles)
    assert res.vertices == [(0, 0), (1, 0), (0, 1)]


def test_triangulator_triangle_indices_are_valid_for_square():
    """Vérifie que les indices de triangles sont dans les bornes."""
    tri = Triangulator()

    def _get_pointset_square(point_set_id):
        return {"id": PointSet(points=[(0, 0), (1, 0), (1, 1), (0, 1)])}[point_set_id]

    tri.get_PointSet = _get_pointset_square

    res = tri.triangulate("id")

    for (a, b, c) in res.triangles:
        assert 0 <= a < 4
        assert 0 <= b < 4
        assert 0 <= c < 4


def test_encode_triangles_return_bytes():
    """Vérifie que encode_triangles renvoie bien des bytes."""
    tri = Triangulator()
    triangles = Triangles(vertices=[(0, 0), (1, 0), (0, 1)],triangles=[(0, 1, 2)],)

    encoded = tri.encode_triangles(triangles)
    assert isinstance(encoded, bytes)
    assert len(encoded) > 0


def test_parse_pointset_empty_bytes_return_empty_pointset():
    """Vérifie que parse_pointset décode bien un PointSet vide."""
    tri = Triangulator()

    empty_bytes = (0).to_bytes(4, "little", signed=False)

    pointset = tri.parse_pointset(empty_bytes)
    assert isinstance(pointset, PointSet)
    assert pointset.points == []

def test_pointset_to_bytes_header_and_points():
    """Vérifie que to_bytes encode bien le header et les points."""
    ps = PointSet(points=[(1.0, 2.5), (-3.0, 4.0)])
    data = ps.to_bytes()

    # verifie que c est bien des bytes
    assert isinstance(data, bytes)

    # header doit être égal au nombre de points, 2
    header = data[:4]
    assert header == (2).to_bytes(4, "little")

    x1 = struct.pack("<f", 1.0)
    y1 = struct.pack("<f", 2.5)

    x2 = struct.pack("<f", -3.0)
    y2 = struct.pack("<f", 4.0)

    attendu = (2).to_bytes(4, "little") + x1 + y1 + x2 + y2

    # verifie que tout est identique
    assert data == attendu
def test_encode_triangles_simple():
    """Vérifie que encode_triangles produit bien le binaire attendu pour un triangle."""
    tri = Triangulator()
    verts = [(0.0,0.0),(1.0,0.0),(0.0,1.0)]
    tris = [(0,1,2)]
    t = Triangles(vertices=verts, triangles=tris)

    data = tri.encode_triangles(t)
    assert isinstance(data, bytes)

    header_v = (3).to_bytes(4,"little")
    v0 = struct.pack("<f",0.0)+struct.pack("<f",0.0)
    v1 = struct.pack("<f",1.0)+struct.pack("<f",0.0)
    v2 = struct.pack("<f",0.0)+struct.pack("<f",1.0)
    header_t = (1).to_bytes(4,"little")

    tri_b = (0).to_bytes(4,"little")+(1).to_bytes(4,"little")+(2).to_bytes(4,"little")

    attendu = header_v + v0 + v1 + v2 + header_t + tri_b
    assert data == attendu
