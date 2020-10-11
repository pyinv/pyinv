.PHONY: all clean lint type test test-cov

CMD:=poetry run
PYMODULE:=srohub
TESTS:=

all: lint 

lint: 
	$(CMD) flake8 $(PYMODULE) $(TESTS)

type: 
	$(CMD) mypy $(PYMODULE) $(TESTS) 

test:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

test-cov:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report html

test-ci:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report xml

isort:
	$(CMD) isort $(PYMODULE) $(TESTS)

clean:
	git clean -Xdf # Delete all files in .gitignore
