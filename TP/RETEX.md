# RETEX - Retour d'expérience sur le projet

Je me suis appercu au cours de l'étape 2 que le plan n'était pas conforme car je n'avais pas bien suivi la trace dans `triangulator.yml`


## Ce qui a bien marché 

- J'ai réussi à faire passer tous les tests (unitaires, intégration et perf). Les tests sont fiables et rapides.
- J'ai configuré et exécuté `ruff` pour la vérification de style et corrigé la plupart des problèmes.
- J'ai écrit des fonctions manquantes (sérialisation des PointSet, parsing, encodage de triangles, triangulation simple) pour que le code soit utilisable.
- J'ai généré la documentation HTML avec `pdoc`.

## Ce qui a moins bien marché 

- La vérification des docstrings avec `ruff` a posé des difficultés car le projet devait utiliser des docstrings en français. Certaines règles (ex: D401) supposent une forme impérative en anglais et ne s'appliquent pas bien au français.
- J'ai dû ajuster la configuration de `ruff` (ajout d'une exception pour D401) pour accepter les docstrings en français.
- La génération de la doc (`pdoc`) nécessitait des imports package-qualifiés (`TP.models` au lieu de `models`) pour que pdoc puisse importer correctement le package.

## Ce que je ferais différemment avec le recul 

- 
- suivre l'énoncé attentivement dès le début, car cela m'a fait perdre beaucoup de temps 
- Mettre dès le début des imports package qualifiés (par eemple: `from TP.models import `) pour éviter des problèmes lors de l'utilisation d'outils qui importent le package (doc generators, type checkers, etc.)
- mettre en place une convention claire pour la langue des docstrings
-


## Structure du projet et explications

- Emplacement des fichiers principaux :
  - `TP/tests/` : contient les tests unitaires, d'intégration, d'api et de performance :
    - `test_triangulator_unit.py` : tests unitaires pour la logique de triangulation 
    - `test_triangulator_intergration.py` : tests d'intégration de l'enchaînement PointSetManager -> Triangulator ->  Api Flask
    - `test_triangulator_perf.py` : tests de performance pour mesurer le comportement sur de plus grands jeux de données
  - `TP/models.py` : définit les modèles de données `PointSet` et `Triangles`
  - `TP/Triangulator.py` : classe `Triangulator` qui fournit plusieurs responsabilités :
    - `get_pointset` / `get_PontSet` : récupération d'un `PointSet`
    - `parse_pointset(data: bytes)` : décode un `PointSet` à partir de bytes 
    - `triangulate(point_set_id)` : calcule une triangulation
    - `encode_triangles(triangles: Triangles)` : encode l'objet `Triangles` au format binaire 
    - `create_app(triangulator)` : fabrique une app Flask avec `/triangulate/<point_set_id>` qui renvoie les triangles encodés en binaire

- Ce que les tests les testent :
  - Les tests unitaires vérifient le comportement interne de `triangulate` (cas limites, duplications, colinéarité), `encode_triangles`, et `PointSet.to_bytes`.
  - les tests d'intégration valident l'enchaînement complet (manager -> triangulate -> API) et les réponses de l'API (format binaire, codes d'erreusr)
  - les tests de perf mesurent la robustesse et le temps d'exécution sur des données plus volumineuses.


## Sorties des commandes `make`

Voici les sorties complètes des commandes que j'ai exécutées pendant cette séance.

### make test

```
../env/bin/pytest TP/tests
======================================= test session starts ========================================
platform darwin -- Python 3.10.19, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/aymanearbai/Documents/cours/S7/tech_test/techniques_de_test_2025_2026
configfile: pyproject.toml
collected 26 items                                                                                 

TP/tests/test_triangulator_intergration.py ..........                                        [ 38%]
TP/tests/test_triangulator_perf.py ....                                                      [ 53%]
TP/tests/test_triangulator_unit.py ............                                              [100%]

======================================== 26 passed in 0.17s ========================================
```

### make unit_test

```
../env/bin/pytest -m "not perf" TP/tests
======================================= test session starts ========================================
platform darwin -- Python 3.10.19, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/aymanearbai/Documents/cours/S7/tech_test/techniques_de_test_2025_2026
configfile: pyproject.toml
collected 26 items / 4 deselected / 22 selected                                                     

TP/tests/test_triangulator_intergration.py ..........                                        [ 45%]
TP/tests/test_triangulator_unit.py ............                                              [100%]

================================= 22 passed, 4 deselected in 0.12s =================================
```

### make perf_test

```
../env/bin/pytest -m perf TP/tests
======================================= test session starts ========================================
platform darwin -- Python 3.10.19, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/aymanearbai/Documents/cours/S7/tech_test/techniques_de_test_2025_2026
configfile: pyproject.toml
collected 26 items / 22 deselected / 4 selected                                                     

TP/tests/test_triangulator_perf.py ....                                                      [100%]

================================= 4 passed, 22 deselected in 0.11s =================================
```

### make lint

```
../env/bin/ruff check .
warning: `incorrect-blank-line-before-class` (D203) and `no-blank-line-before-class` (D211) are incompatible. Ignoring `incorrect-blank-line-before-class`.
warning: `multi-line-summary-first-line` (D212) and `multi-line-summary-second-line` (D213) are incompatible. Ignoring `multi-line-summary-second-line`.
All checks passed!
```

> Note: j'ai dû ajouter `extend-ignore = ["D401"]` dans `pyproject.toml` parce que D401 vérifie la forme impérative en anglais et n'est pas adaptée aux docstrings en français.

### make coverage

```
../env/bin/coverage run -m pytest TP/tests
====================================== test session starts ======================================
platform darwin -- Python 3.10.19, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/aymanearbai/Documents/cours/S7/tech_test/techniques_de_test_2025_2026
configfile: pyproject.toml
collected 26 items                                                                               

TP/tests/test_triangulator_intergration.py ..........                                     [ 38%]
TP/tests/test_triangulator_perf.py ....                                                   [ 53%]
TP/tests/test_triangulator_unit.py ............                                           [100%]

====================================== 26 passed in 0.19s =======================================
../env/bin/coverage html -d coverage_html
Wrote HTML report to coverage_html/index.html
Coverage report generated in coverage_html/index.html
```

### make doc

```
../env/bin/pdoc --html TP --output-dir docs --force
docs/TP/index.html
docs/TP/Triangulator.html
docs/TP/app.html
docs/TP/models.html
docs/TP/pointset.html
docs/TP/pointset_manager_client.html
docs/TP/tests/index.html
docs/TP/tests/conftest.html
docs/TP/tests/test_triangulator_api.html
docs/TP/tests/test_triangulator_intergration.html
docs/TP/tests/test_triangulator_perf.html
docs/TP/tests/test_triangulator_unit.html
Docs generated in docs/
```

## Détail des tests par fichier

Pour chaque fichier de test, voici simplement ce que vérifie chaque fonction :

- `TP/tests/test_triangulator_unit.py` :
  - `test_triangulate_small_pointset` : vérifie qu'on n'a pas de triangle pour 0, 1 ou 2 points.
  - `test_triangulator_three_points_non_aligned` : vérifie que 3 points non alignés donnent un triangle.
  - `test_triangulator_three_points_aligned` : vérifie que 3 points alignés ne donnent aucun triangle.
  - `test_triangulator_invalid_values` : vérifie que des valeurs invalides n'empêchent pas l'exécution et ne donnent pas de triangle.
  - `test_triangulator_duplicated_points` : vérifie que des points dupliqués n'engendrent pas de triangle incorrect.
  - `test_triangulator_four_points_square` : vérifie que 4 points forment bien 2 triangles.
  - `test_triangulator_returns_triangles_object` : vérifie que la fonction renvoie un objet `Triangles` avec les sommets.
  - `test_triangulator_triangle_indices_are_valid_for_square` : vérifie que les indices des triangles sont dans les bornes.
  - `test_encode_triangles_return_bytes` : vérifie que `encode_triangles` renvoie des bytes.
  - `test_parse_pointset_empty_bytes_return_empty_pointset` : vérifie que `parse_pointset` décode correctement un PointSet vide.
  - `test_pointset_to_bytes_header_and_points` : vérifie que `PointSet.to_bytes` encode bien le header et les points.
  - `test_encode_triangles_simple` : vérifie que `encode_triangles` produit le binaire attendu pour un triangle simple.

- `TP/tests/test_triangulator_intergration.py` :
  - `FakePointSetManager` : simule le stockage/récupération de PointSet pour les tests.
  - `test_integration_full_triangulation` : vérifie le flux complet client -> manager -> triangulator -> triangles.
  - `test_integration_results_match_original_points` : vérifie que les indices des triangles pointent vers les points d'origine.
  - `test_integration_multiple_pointsets` : vérifie que plusieurs triangulations successives fonctionnent.
  - `test_integration_unknown_pointset_id` : vérifie le comportement quand l'id de pointset est inconnu.
  - `test_api_triangulate` : vérifie que l'API renvoie des bytes et un code 200 pour un PointSet valide.
  - `test_api_triangulate_unknown_id` : vérifie que l'API renvoie une erreur JSON quand l'id est inconnu.
  - `test_api_triangulate_empty_pointset` : vérifie que l'API renvoie des bytes même pour un PointSet vide.
  - `test_api_triangulate_bad_id_format` : vérifie que l'API renvoie 400 pour un mauvais format d'id.
  - `test_api_triangulate_not_found` : vérifie que l'API renvoie 404 si le PointSet n'est pas trouvé.
  - `test_api_triangulate_manager_unavailable` : vérifie que l'API renvoie 503 si le manager est indisponible.

- `TP/tests/test_triangulator_perf.py` :
  - `test_perf_triangulate_100_points` : mesure le temps pour 100 points (doit être rapide).
  - `test_perf_triangulate_1000_points` : mesure le temps pour 1000 points (doit être rapide).
  - `test_perf_encode_triangles` : mesure la vitesse d'encodage des triangles.
  - `test_scaling_triangulate_linear` : vérifie que le temps par point reste raisonnable quand la taille augmente.

- `TP/tests/test_triangulator_api.py` : fichier sans tests (actuellement vide).

## Conclusion

- J'ai réussi à stabiliser le projet : tests verts, linter vert, documentation générée
- Les choix à améliorer : définir une convention de langue pour les docstrings et des imports package-qualifiés dès le départ
