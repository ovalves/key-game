# key-game

## Desenvolvimento

Para instalar as dependências do projeto utilize o `virutal env`.

```bash
python -m venv venv
source venv/bin/activate
```

Execute o comando para instalar as dependências
```bash
make
```

### Formatação de código
O código segue o padrão do `black`. Para formatar o código, use o comando:

```
make code_formatter
```

## Testes Unitários
Para executar os testes unitários execute o comando:

```
make test
```

O relatório detalhado com a cobertura dos testes fica em `htmlcov/index.html`.

* Player vs IA game built using PyGame

* Must have Python 3.8 and Pygame 1.9.6 installed.

### Installation Instructions

> Run the following commands
```commandline
pip install -r requirements.txt
python src/Main.py
```