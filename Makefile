SHELL := /bin/bash
PYTHON = python3

.PHONY = run-backend create-env

create-env:
	${PYTHON} -m venv env

install-backend:
	source env/bin/activate && cd backend && pip install -r requirements.txt

run-backend:
	source env/bin/activate && flask run

compile-client:
	npm run build -- --watch

clean-pyc:
	find . -name '*.pyc' -delete
	find . -type d -name "__pycache__" -delete

test-backend:
	source env/bin/activate && python -m pytest