migrations:
	python manage.py makemigrations backend

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
