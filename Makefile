install:
	pip install -r requirements-dev.txt

run:
	python run.py

test:
	pytest

coverage:
	pytest --cov=multi_credit tests/ --cov-branch

flake8:
	flake8 --max-line-length=119 --exclude=.venv .
