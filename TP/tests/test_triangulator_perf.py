"""Tests de performance pour le triangulateur."""

import statistics
import time

import pytest

from TP.models import PointSet, Triangles
from TP.Triangulator import Triangulator

pytestmark = pytest.mark.perf  


def test_perf_triangulate_100_points():
    """Test la vitesse de triangulate sur 100 points."""
    # crée 100 points simples
    points = []
    for i in range(100):
        points.append((i * 0.1, i * 0.1))

    tri = Triangulator()
    tri.get_pointset = lambda pid: PointSet(points=points)

    start = time.time()
    res = tri.triangulate("x")
    end = time.time()

    # vérifie juste que ça renvoie bien des triangles
    assert isinstance(res, Triangles)

    assert (end - start) < 0.5  # moins d'une demi seconde



def test_perf_triangulate_1000_points():
    """Test la vitesse de triangulate sur 1000 points."""
    # crée 1000 points simples
    points = []
    for i in range(1000):
        points.append((i * 0.1, i * 0.1))

    tri = Triangulator()
    tri.get_pointset = lambda pid: PointSet(points=points)

    start = time.time()
    res = tri.triangulate("x")
    end = time.time()

    # vérifie juste que ça renvoie bien des triangles
    assert isinstance(res, Triangles)

    assert (end - start) < 1  # moins d'une seconde


def test_perf_encode_triangles():
    """Test la vitesse de encode_triangles."""
    verts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    tris = [(0, 1, 2)]

    obj = Triangles(sommets=verts, triangles=tris)

    tri = Triangulator()

    start = time.time()
    data = tri.encode_triangles(obj)
    end = time.time()

    # encode doit renvoyer des bytes
    assert isinstance(data, bytes)

    assert (end - start) < 0.2


def test_scaling_triangulate_linear():
    """Vérifie que le temps de 'triangulate' croît linéairement.

    On mesure le temps pour plusieurs tailles (100, 1000, 5000, 10000 points)
    et on compare le temps par point. Si l'écart entre le plus lent et le plus
    rapide est inférieur à 3x alors on considère que la croissance est linéaire.
    """
    sizes = [100, 1000, 5000, 10000]
    runs_per_size = 5
    median_times = []

    for n in sizes:
        points = [(i * 0.1, i * 0.1) for i in range(n)]

        tri = Triangulator()
        tri.get_pointset = lambda pid, pts=points: PointSet(points=pts)

        run_times = []
        for _ in range(runs_per_size):
            start = time.perf_counter()
            res = tri.triangulate("x")
            end = time.perf_counter()

            assert isinstance(res, Triangles)
            run_times.append(end - start)

        median_times.append(statistics.median(run_times))

    rates = [t / n for t, n in zip(median_times, sizes, strict=True)]

    # le max/min des temps par point ne doit pas dépasser 2x
    assert max(rates) / min(rates) < 2
