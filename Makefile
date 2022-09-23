deps:
	pip3 install -r requirements.txt
	pip3 install -r requirements.dev.txt

test:
	nose2 -v --with-coverage --coverage-report html --coverage-report term --coverage-report xml

code_formatter:
	black src

start:
	python src/Main.py
