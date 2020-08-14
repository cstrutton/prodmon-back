.PHONY : clean test
clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.sql' -exec rm --force {} +

init:
	# pipenv install -r requirements.txt

test:
	pytest tests

