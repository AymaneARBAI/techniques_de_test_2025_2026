"""Utilitaires du Triangulator.

Définit la classe Triangulator pour la triangulation de PointSet.
"""

from flask import Flask, Response

from TP.models import PointSet, Triangles


class Triangulator:
    """Calculer des triangulations et encoder des ensembles de triangles."""

    def __init__(self):
        """Initialise une nouvelle instance de Triangulator."""
        pass

    def encode_triangles(self, triangles: Triangles) -> bytes:
        """Encode les triangles en format binaire.

        Format :
        - 4 octets little-endian (entier non signé) : nombre de sommets
        - pour chaque sommet : 4 octets float x, 4 octets float y (little-endian)
        - 4 octets little-endian (entier non signé) : nombre de triangles
        - pour chaque triangle : 3 × 4 octets little-endian indices
        """
        import struct

        out = len(triangles.vertices).to_bytes(4, "little")
        for x, y in triangles.vertices:
            out += struct.pack("<f", float(x))
            out += struct.pack("<f", float(y))

        out += len(triangles.triangles).to_bytes(4, "little")
        for a, b, c in triangles.triangles:
            out += int(a).to_bytes(4, "little")
            out += int(b).to_bytes(4, "little")
            out += int(c).to_bytes(4, "little")
        return out

    def get_pointset(self, point_set_id: str) -> PointSet:
        """Récupérer un PointSet par son identifiant (API en snake_case).

        Cette méthode supporte le remplacement au niveau de l'instance (monkeypatch)
        en utilisant soit `get_pointset` soit l'ancien nom `get_PointSet`.
        """
        # allow instance-level overrides (monkeypatching)
        gp = self.__dict__.get("get_pointset")
        if gp is not None and gp is not Triangulator.get_pointset:
            try:
                return gp(point_set_id)
            except TypeError:
                return gp()[point_set_id]

        gpc = self.__dict__.get("get_PointSet")
        if gpc is not None and gpc is not Triangulator.get_pointset:
            try:
                return gpc(point_set_id)
            except TypeError:
                return gpc()[point_set_id]

        raise NotImplementedError

    get_PointSet = get_pointset

    def parse_pointset(self, data: bytes) -> PointSet:
        """Analyser des données binaires pour produire un PointSet."""
        from pointset import parse_pointset

        return parse_pointset(data)

    def triangulate(self, point_set_id) -> Triangles:  
        """Calculer une triangulation simple pour l'identifiant de PointSet fourni.

        L'implémentation est volontairement simple : pour n > 2 nous utilisons une
        triangulation en éventail à partir du sommet 0 (triangles (0, i, i+1)).
        Les cas particuliers pour 0-2 points et 3 points colinéaires sont gérés.
        """
        ps = self.get_pointset(point_set_id)

        cleaned: list[tuple[float, float]] = []
        seen = set()
        for p in ps.points:
            try:
                x, y = float(p[0]), float(p[1])
            except Exception:
                continue
            key = (x, y)
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(key)

        n = len(cleaned)
        if n < 3:
            return Triangles(vertices=cleaned, triangles=[])

        def _area(a, b, c):
            return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

        if n == 3:
            if _area(cleaned[0], cleaned[1], cleaned[2]) == 0:
                return Triangles(vertices=cleaned, triangles=[])
            return Triangles(vertices=cleaned, triangles=[(0, 1, 2)])

        tris = [(0, i, i + 1) for i in range(1, n - 1)]
        return Triangles(vertices=cleaned, triangles=tris)



def create_app(triangulator):
    """Créer une application Flask exposant les endpoints de l'API de triangulation."""
    app = Flask(__name__)

    @app.get("/triangulate/<point_set_id>")
    def triangulate_api(point_set_id):
        try:
            res = triangulator.triangulate(point_set_id)
            data = triangulator.encode_triangles(res)
            return Response(data, mimetype="application/octet-stream")
        except KeyError:
            return {"error": "notfound"}, 404
        except Exception:
            return {"error": "error"}, 500

    return app
