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
	python src/models.py

scrap-data:
	python src/tasks.py

