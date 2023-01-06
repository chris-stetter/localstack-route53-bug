#!/bin/bash

# Run git inside virtual environment; this is only necessary inside the VSC SCM Panel; otherwise normal git is used
source /nefino_li/dist/export/python/virtualenvs/default/$PYTHON_VERSION/bin/activate || echo "Sourcing of venv failed."

exec git $@
