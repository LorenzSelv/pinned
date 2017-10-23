
tests:
	python manage.py test core

cleandb:
	-rm db.sqlite3
	-rm core/migrations/0001_initial.py
	-rm core/migrations/__pycache__/*

db: cleandb
	python manage.py makemigrations core
	python manage.py migrate
	python test_util/create_sample_db.py