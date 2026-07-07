.PHONY: up down backend frontend test seed reset logs

## Start the full stack (Postgres + Redis + backend + frontend)
up:
	docker compose -f infra/docker-compose.yml up

## Start in detached mode
up-d:
	docker compose -f infra/docker-compose.yml up -d

## Stop all services
down:
	docker compose -f infra/docker-compose.yml down

## Run the backend locally (requires Python + deps installed)
backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Run the frontend locally
frontend:
	cd frontend && npm run dev

## Run backend tests
test:
	cd backend && pytest tests/ -v

## Seed demo data for the 5 beats
seed:
	python scripts/seed_demo_data.py --base-url http://localhost:8000

## Verify all 5 demo beats
verify:
	python scripts/replay_demo_beats.py --base-url http://localhost:8000

## Reset demo state
reset:
	curl -X POST http://localhost:8000/demo/reset

## View backend logs
logs:
	docker compose -f infra/docker-compose.yml logs -f backend

## Production deploy
prod-up:
	docker compose -f infra/docker-compose.yml -f infra/docker-compose.prod.yml up -d --build
