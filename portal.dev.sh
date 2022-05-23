#!/bin/bash
echo "Entrando na pasta do projeto"
cd app
pwd
echo "Criando ambiente virtual"
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt