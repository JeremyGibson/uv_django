
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


run-dev:
	@echo 'Running local development'
	docker compose up -d --remove-orphans
	bun run dev &
	python manage.py runserver

run-tests:
	@echo 'Checking for migrations'
	python manage.py makemigrations --dry-run --check
	pytest
