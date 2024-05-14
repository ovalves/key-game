help:
	@echo ""
	@echo "Commands:"
	@echo "  deps               Instalar todas as dependências do projeto"
	@echo "  test               Rodar todos os testes do projeto"
	@echo "  start              Iniciar todos os serviços do projeto"
	@echo "  pylint             Validar a qualidade do código"
	@echo "  build-venv         Criar o ambiente virtual"
	@echo "  start-venv         Iniciar o ambiente virtual"
	@echo "  code-formatter     Formatar o código do projeto"

deps:
	pip3 install -r requirements.txt
	pip3 install -r requirements.dev.txt

test:
	nose2 -v --with-coverage --coverage-report html --coverage-report term --coverage-report xml

code-formatter:
	black src

pylint:
	pylint ./src

build-venv:
	python -m venv venv

start-venv:
	@source venv/bin/activate

start:
	python src/Main.py
