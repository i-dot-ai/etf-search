include envs/web

define _update_requirements
	docker-compose run requirements bash -c "pip install -U pip setuptools && pip install -U -r /app/$(1).txt && pip freeze > /app/$(1).lock"
endef

.PHONY: update-requirements
update-requirements:
	$(call _update_requirements,requirements)
	$(call _update_requirements,requirements-dev)

.PHONY: reset-db
reset-db:
	docker-compose up --detach ${POSTGRES_HOST}
	docker-compose run ${POSTGRES_HOST} dropdb -U ${POSTGRES_USER} -h ${POSTGRES_HOST} ${POSTGRES_DB}
	docker-compose run ${POSTGRES_HOST} createdb -U ${POSTGRES_USER} -h ${POSTGRES_HOST} ${POSTGRES_DB}
	docker-compose kill

.PHONY: add-fake-data
add-fake-data:
	docker-compose build web
	docker-compose run web python manage.py add_fake_data

# -------------------------------------- Code Style  -------------------------------------

.PHONY: check-python-code
check-python-code:
	isort --check .
	black --check .
	flake8

.PHONY: check-migrations
check-migrations:
	docker-compose build web
	docker-compose run web python manage.py migrate
	docker-compose run web python manage.py makemigrations --check

.PHONY: test
test:
	docker-compose down
	docker-compose build tests-etf etf-test-db && docker-compose run --rm tests-etf
	docker-compose down
