test:
	pytest --verbose --color=yes 

run:
	FLASK_APP=app.py flask run

debug:
	FLASK_APP=app.py FLASK_ENV=development flask run
