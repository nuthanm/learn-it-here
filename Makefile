.PHONY: help install run test lint fmt check clean

help:
	@echo "Targets:"
	@echo "  install   Install runtime + dev dependencies"
	@echo "  run       Start the Streamlit app on http://localhost:8501"
	@echo "  test      Run the pytest suite"
	@echo "  lint      Run ruff lint checks"
	@echo "  fmt       Format the codebase with ruff"
	@echo "  check     Run lint + tests (the CI gate)"
	@echo "  clean     Remove caches and build artefacts"

install:
	pip install -e ".[dev]"

run:
	streamlit run app.py

test:
	pytest

lint:
	ruff check .

fmt:
	ruff format .
	ruff check --fix .

check: lint test

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
