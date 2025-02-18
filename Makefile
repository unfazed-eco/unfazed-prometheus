all: test

test:
	@echo "Running tests..."
	uv run pytest -v -s --cov ./unfazed_prometheus --cov-report term-missing

format:
	@echo "Formatting code..."
	ruff format tests/ unfazed_prometheus/
	ruff check tests/ unfazed_prometheus/  --fix
	mypy --check-untyped-defs --explicit-package-bases tests/ unfazed_prometheus/

publish:
	@echo "Publishing package..."
	uv build
	uv publish
