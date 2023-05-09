all: clear_db clear_migrations migrate superuser runserver

clear_db:
	rm -rf db.sqlite3

clear_migrations:
	rm -rf */migrations/0*

clear: clear_db clear_migrations

runserver:
	python manage.py runserver 8001

migrate:
	python manage.py makemigrations
	python manage.py migrate

superuser:
	python manage.py createsu