#!/bin/bash
source venv/bin/activate
pip install --upgrade pip
pip install ipython ipyparallel
ipcluster nbextension enable
ipython profile create
ipcluster start
pip show ipython ipyparallel
pip install jupyterlab
pip freeze > requirements
jupyter lab
