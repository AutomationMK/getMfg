#!/bin/bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
playwright install chromium
deactivate
read -p "Press Enter to close the window..."
