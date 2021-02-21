build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose build

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down

test:
	docker exec api bash -c "python -m pytest tests -v --cov=app --cov-fail-under=70 --cov-config=.coveragerc -s"

test-unit:
	docker exec api bash -c "python -m pytest tests/unit -v --cov-config=.coveragerc -s"

test-integration:
	docker exec api bash -c "python -m pytest tests/integration -v -config=.coveragerc -s"

.PHONY: all test clean
