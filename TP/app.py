"""Factory Flask pour l'API de triangulation.

Fournit un endpoint HTTP pour demander la triangulation d'un PointSet par identifiant.
"""

from flask import Flask, Response, jsonify


def create_app(triangulator):
    """Créer une application Flask exposant les endpoints de l'API de triangulation."""
    app = Flask(__name__)

    @app.get("/triangulate/<point_set_id>")
    def triangulate_api(point_set_id):
        try:
            res = triangulator.triangulate(point_set_id)
            data = triangulator.encode_triangles(res)
            return Response(data, mimetype="application/octet-stream")
        except KeyError as e:
            msg = str(e) if str(e) else "PointSet not found"
            return jsonify({"code": "NOT_FOUND", "message": msg}), 404
        except ValueError as e:
            msg = str(e) if str(e) else "Bad request"
            return jsonify({"code": "BAD_REQUEST", "message": msg}), 400
        except ConnectionError as e:
            msg = str(e) if str(e) else "Service unavailable"
            return jsonify({"code": "SERVICE_UNAVAILABLE", "message": msg}), 503
        except Exception as e:
            msg = str(e) if str(e) else "Internal server error"
            return jsonify({"code": "INTERNAL_ERROR", "message": msg}), 500

    return app
