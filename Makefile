all: safety bandit mypy pylint pytest
restart: down up
init: create-tables scrap-data


### Compose shortcuts
up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

sh:
	docker-compose run -p 5000:5000 --rm app_launch bash

logs:
	docker-compose logs -f

psql:
	docker-compose exec postgres psql -U postgres


### Project shortcuts
create-tables:
	docker-compose run --rm app_launch python src/scrapping/models.py

scrap-data:
	docker-compose run --rm app_launch python src/scrapping/tasks.py

celery:
	docker-compose run --rm app_launch celery -E -A root worker --beat --loglevel=info

### Linters
safety:
	@docker-compose run --rm app_launch safety check --full-report

bandit:
	@docker-compose run --rm app_launch bandit -c bandit.yml -r src

pylint:
	@docker-compose run --rm app_launch pylint src

mypy:
	@docker-compose run --rm app_launch mypy src

pytest:
	@docker-compose run --rm -e DB_URL=postgres://postgres@postgres:5432/tests app_launch pytest -ra --cov=src
