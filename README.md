# Ordering

Aplicación utilizada en la cursada 2018 de Ingenieria de Software. UTN-FRLP

## Dependencias

- python 3
- flask
- sqlite

## Instalar dependencias

`pip install -r requirements.txt`

## Iniciar la Base de Datos

En Linux

```bash
export FLASK_APP=orderingg.py
flask db upgrade
python fixture.py
```

En Windows

-cmd
```bash
set FLASK_APP=orderingg.py
flask db upgrade
python fixture.py
```

-PowerShell
```bash
$env:FLASK_APP="orderingg.py"
flask db upgrade
python fixture.py
```

## Iniciar app

En Linux

```bash
export FLASK_APP=orderingg.py
export FLASK_DEBUG=1
flask run
```

En Windows

-cmd
```bash
set FLASK_APP=orderingg.py
set FLASK_DEBUG=1
flask run
```

-PowerShell
```bash
$env:FLASK_APP="orderingg.py"
$env:FLASK_DEBUG="1"
flask run
```

Grupo 2
```bash
Nahuel Baez
Leonardo Frison
Carlos Andrade
```
