
clean:
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "__pycache__" -delete


update_requirements:
	uv sync

install_requirements:
	uv sync

setup:
	@echo 'Setting up the environment...'
	make install_requirements

run-prod:
	@echo "Running the production server"
	docker compose -f docker-compose-deploy.yml up -d

run-dev-db:
	@echo "Starting local db"
	docker compose up -d --remove-orphans

run-dev:
	@echo 'Running local development'
	docker compose up -d --remove-orphans
	bun run build.config.js &
	python manage.py runserver

run-tests:
	@echo 'Checking for migrations'
	python manage.py makemigrations --dry-run --check
	pytest
