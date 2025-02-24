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


client:
	@echo "Running prometheus client..."
	uv run uvicorn scripts.prometheus_client:app --reload --port 9527 --host 0.0.0.0
