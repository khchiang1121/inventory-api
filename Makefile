include .env
export
install-mamba:
	mamba install --yes --file requirements.txt

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

test:
	python manage.py test virtflow.api.tests

run:
	python manage.py runserver 0.0.0.0:8201

production:
	uvicorn virtflow.asgi:application --host 0.0.0.0 --port 8200

production-gunicorn:
	gunicorn virtflow.wsgi:application --bind 0.0.0.0:8200

stage:
	python manage.py runserver 0.0.0.0:8201

fake:
	python manage.py generate_fake_data

flush:
	python manage.py flush

reset:
	python manage.py reset_db --noinput
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	python manage.py makemigrations
	python manage.py migrate
	python manage.py createsuperuser --noinput
	python manage.py generate_fake_data
	@echo "Creating token for $(DJANGO_SUPERUSER_USERNAME)"
	@python manage.py shell -c "from django.contrib.auth import get_user_model; from rest_framework.authtoken.models import Token; User = get_user_model(); user = User.objects.get(username='$(DJANGO_SUPERUSER_USERNAME)'); token, _ = Token.objects.get_or_create(user=user); print(token.key)"
	@echo "Creating token for user"
	@python manage.py shell -c "from django.contrib.auth import get_user_model; from rest_framework.authtoken.models import Token; User = get_user_model(); user = User.objects.get(username='user'); Token.objects.update_or_create(user=user, defaults={'key': 'my-static-token-123456'}); print('my-static-token-123456')"


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