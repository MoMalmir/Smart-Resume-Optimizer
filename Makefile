install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

test:
	python -m pytest -vv test_*.py

format:
	black backend/*.py

lint:
	pylint --disable=R,C backend/*.py

all: install lint test