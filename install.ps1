python -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
playwright install chromium
deactivate
Read-Host -Prompt "Press Enter to close the window..."
