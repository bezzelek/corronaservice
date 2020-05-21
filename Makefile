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
