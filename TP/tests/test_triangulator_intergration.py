"""Integration tests for the Triangulator API and helpers."""

from TP.app import create_app
from TP.models import PointSet, Triangles
from TP.Triangulator import Triangulator


class FakePointSetManager:
    """Simule un PointSetManager pour les tests d'intégration."""

    def __init__(self):
        """Create an empty fake manager."""
        self.data = {}

    def save(self, point_set_id: str, pointset: PointSet):
        """Enregistre un PointSet avec son id."""
        self.data[point_set_id] = pointset

    def get(self, point_set_id: str) -> PointSet:
        """Récupère un PointSet à partir de son id."""
        return self.data[point_set_id]


def test_integration_full_triangulation():
    """Client -> PointSetManager -> Triangulator -> Triangles."""
    manager = FakePointSetManager()
    triangulator = Triangulator()

    # Le client envoie un ensemble de points au PointSetManager
    pointset = PointSet(points=[(0, 0), (1, 0), (0, 1)])
    manager.save("ps1", pointset)

    # le Triangulator récupere le PointSet 
    triangulator.get_pointset = lambda point_set_id: manager.get(point_set_id)

    # Triangulation
    res = triangulator.triangulate("ps1")

    # Vérifications simples
    assert isinstance(res, Triangles)
    assert res.sommets == pointset.points
    assert len(res.triangles) >= 0  # au moins pas d'erreur


def test_integration_results_match_original_points():
    """Vérifie que les triangles renvoyés utilisent bien les points d'origine."""
    manager = FakePointSetManager()
    triangulator = Triangulator()

    original_points = PointSet(points=[(0, 0), (1, 0), (1, 1), (0, 1)])
    manager.save("ps2", original_points)

    triangulator.get_pointset = lambda point_set_id: manager.get(point_set_id)
    res = triangulator.triangulate("ps2")

    # chaque indice de triangle doit pointer vers un sommet existant
    for (a, b, c) in res.triangles:
        assert 0 <= a < len(original_points.points)
        assert 0 <= b < len(original_points.points)
        assert 0 <= c < len(original_points.points)


def test_integration_multiple_pointsets():
    """Vérifie que plusieurs triangulations successives continuent de marcher."""
    manager = FakePointSetManager()
    triangulator = Triangulator()

    triangulator.get_pointset = lambda point_set_id: manager.get(point_set_id)

    # on enregistre plusieurs ensembles de points
    manager.save("small", PointSet(points=[(0, 0), (1, 0), (0, 1)]))
    manager.save("square", PointSet(points=[(0, 0), (1, 0), (1, 1), (0, 1)]))

    res1 = triangulator.triangulate("small")
    assert isinstance(res1, Triangles)
    assert res1.sommets == manager.get("small").points

    res2 = triangulator.triangulate("square")
    assert isinstance(res2, Triangles)
    assert res2.sommets == manager.get("square").points

    # on vérifie que chaque appel utilise bien les bons points
    assert res1.sommets != res2.sommets


def test_integration_unknown_pointset_id():
    """Vérifie le comportement quand l'id n'existe pas dans le manager."""
    manager = FakePointSetManager()
    triangulator = Triangulator()

    triangulator.get_pointset = lambda point_set_id: manager.get(point_set_id)

    try:
        triangulator.triangulate("id_inconnu")
        raise AssertionError("triangulate devrait echouer pour un id inconnu")
    except KeyError:
        assert True



# tests API

def test_api_triangulate():
    """Test GET /triangulate returns binary triangles payload."""
    manager = FakePointSetManager()
    manager.save("ps1", PointSet(points=[(0, 0), (1, 0), (0, 1)]))

    triangulator = Triangulator()
    triangulator.get_pointset = lambda pid: manager.get(pid)

    app = create_app(triangulator)
    client = app.test_client()

    r = client.get("/triangulate/ps1")
    assert r.status_code == 200
    assert isinstance(r.data, bytes)
    assert len(r.data) > 0
    assert r.headers.get("Content-Type", "").startswith("application/octet-stream")


def test_api_triangulate_unknown_id():
    """Test API returns an error for unknown point set id."""
    triangulator = Triangulator()
    triangulator.get_pointset = lambda pid: (_ for _ in ()).throw(KeyError())

    app = create_app(triangulator)
    client = app.test_client()

    r = client.get("/triangulate/inconnu")
    assert r.status_code in (400, 404, 500)
    assert r.is_json
    body = r.get_json()
    assert "code" in body and "message" in body


def test_api_triangulate_empty_pointset():
    """Test API handles empty PointSet returning binary payload."""
    manager = FakePointSetManager()
    manager.save("empty", PointSet(points=[]))

    triangulator = Triangulator()
    triangulator.get_pointset = lambda pid: manager.get(pid)

    app = create_app(triangulator)
    client = app.test_client()

    r = client.get("/triangulate/empty")
    assert r.status_code == 200
    assert isinstance(r.data, bytes)
    assert r.headers.get("Content-Type", "").startswith("application/octet-stream")

def test_api_triangulate_bad_id_format():
    """Test API returns 400 for bad point set id format."""
    triangulator = Triangulator()

    # simuler mauvais format UUID 
    triangulator.get_pointset = lambda pid: (
        (_ for _ in ()).throw(ValueError("bad format"))
    )

    app = create_app(triangulator)
    client = app.test_client()

    r = client.get("/triangulate/ID_MAUVAIS_FORMAT")
    assert r.status_code == 400
    assert r.is_json
    body = r.get_json()
    assert "code" in body and "message" in body


def test_api_triangulate_not_found():
    """Vérifie le code 404 quand le PointSet n'est pas trouvé."""
    triangulator = Triangulator()

    # simuler pointset non trouvé 
    triangulator.get_pointset = lambda pid: (_ for _ in ()).throw(KeyError("not found"))

    app = create_app(triangulator)
    client = app.test_client()

    r = client.get("/triangulate/1z2356")
    assert r.status_code == 404
    assert r.is_json
    body = r.get_json()
    assert "code" in body and "message" in body


def test_api_triangulate_manager_unavailable():
    """Test API returns 503 when the PointSet manager is unavailable."""
    triangulator = Triangulator()

    # simuler manager down
    triangulator.get_pointset = lambda pid: (
        (_ for _ in ()).throw(ConnectionError("down"))
    )

    app = create_app(triangulator)
    client = app.test_client()

    r = client.get("/triangulate/ps1")
    assert r.status_code == 503
    assert r.is_json
    body = r.get_json()
    assert "code" in body and "message" in body


