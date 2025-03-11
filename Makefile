migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:8001

production:
	uvicorn virtflow.asgi:application --host 0.0.0.0 --port 8000
