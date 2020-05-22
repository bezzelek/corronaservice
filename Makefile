all: safety bandit mypy pylint pytest
restart: down up
init: create-tables scrap-data


### Compose shortcuts
up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

psql:
	docker-compose exec postgres psql -U postgres


### Project shortcuts
create-tables:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}/src" python src/scrapping/models.py

scrap-data:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}/src" python src/scrapping/tasks.py

celery:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}/src" celery -E -A root worker --beat --loglevel=info

### Linters
safety:
	@safety check --full-report

bandit:
	@bandit -c bandit.yml -r src

pylint:
	@pylint src

mypy:
	@mypy src

pytest:
	@pytest -ra