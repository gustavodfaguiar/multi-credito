run:
	python run.py

test:
	pytest

coverage:
	pytest --cov=multi_credit tests/ --cov-branch
