SHELL := /bin/bash
PYTHON = python3

.PHONY = run-backend create-env

create-env:
	${PYTHON} -m venv env

install-backend:
	source env/bin/activate && cd backend && pip install -r requirements.txt

run-backend:
	source env/bin/activate && flask run