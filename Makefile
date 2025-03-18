all: test

test:
	@echo "Running tests..."
	uv run pytest -v -s --cov ./unfazed_prometheus --cov-report term-missing

format:
	@echo "Formatting code..."
	uv run ruff format tests/ unfazed_prometheus/
	uv run ruff check tests/ unfazed_prometheus/  --fix
	uv run mypy --check-untyped-defs --explicit-package-bases --ignore-missing-imports tests/ unfazed_prometheus/

publish:
	@echo "Publishing package..."
	uv build
	uv publish


client:
	@echo "Running prometheus client..."
	uv run uvicorn scripts.prometheus_client:app --reload --port 9527 --host 0.0.0.0

setup-env:
	uv run python tests/prj/manage.py init-db
	uv run python tests/prj/manage.py migrate
