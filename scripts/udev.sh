#!/bin/bash

# Activate the venv, run the python code and deactivate the venv

source /opt/dlzpy/.venv/bin/activate

python /opt/dlzpy/dlzpy/__main__.py

deactivate
