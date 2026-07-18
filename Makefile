.PHONY: setup lint format test run-dev docker-up docker-down

setup:
	uv sync --all-extras

lint:
	uv run ruff check .
	uv run mypy backend/

format:
	uv run ruff format .

test:
	uv run pytest --cov=backend backend/tests/

run-dev:
	uv run uvicorn backend.apps.gateway.main:app --reload --port 8000

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
