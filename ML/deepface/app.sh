#!/bin/bash
#echo Creando entorno
#python -m venv venv
echo activando entorno
source venv/bin/activate
pip install --upgrade pip
echo Iniciando Jupyterlab
jupyter lab
