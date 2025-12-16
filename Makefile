# Makefile for common tasks
.PHONY: test unit_test perf_test coverage lint doc

# Use the virtualenv provided at repository root for reproducible tooling
VENV_BIN := ../env/bin
TEST_DIR := TP/tests

test:
	PYTHONPATH=. $(VENV_BIN)/pytest $(TEST_DIR)

unit_test:
	PYTHONPATH=. $(VENV_BIN)/pytest -m "not perf" $(TEST_DIR)

perf_test:
	PYTHONPATH=. $(VENV_BIN)/pytest -m perf $(TEST_DIR)

coverage:
	PYTHONPATH=. $(VENV_BIN)/coverage run -m pytest $(TEST_DIR)
	$(VENV_BIN)/coverage html -d coverage_html
	@echo "Coverage report generated in coverage_html/index.html"

lint:
	$(VENV_BIN)/ruff check .

doc:
	$(VENV_BIN)/pdoc --html TP --output-dir docs --force
	@echo "Docs generated in docs/"
