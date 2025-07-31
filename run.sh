#!/bin/bash

DIR=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")

source $DIR/venv/bin/activate
python $DIR/main.py
deactivate
read -p "Press Enter to close the window..."
