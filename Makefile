migrations:
	python manage.py makemigrations api

migrate:
	python manage.py migrate

test:
	python manage.py test backend.tests

run:
	python manage.py runserver 0.0.0.0:8001

production:
	uvicorn virtflow.asgi:application --host 0.0.0.0 --port 8000

stage:
	python manage.py runserver 0.0.0.0:8001

fake:
	python manage.py generate_fake_data

flush:
	python manage.py flush

reset:
	python manage.py reset_db

reset_migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

changepassword:
	python manage.py changepassword admin

createsuperuser:
	python manage.py createsuperuser

# download static files
download-static:
	python manage.py collectstatic --noinput

# download swagger schema
download-swagger-schema:
	python manage.py spectacular --file static/schema.yaml