# Generate MFG Incomming Daily Report

## Description

This is a simple project to generate the excel file for daily incoming mfg $.
Any unfilled mfg $ will result in a row with red cells to indicate that
it needs to be fixed and updated on E2 and regenerate the report again.

Please note that any unprocessed jobs for the day are a bug that will break the program.
Possibly consider updating a way to handle unprocessed jobs, but for now it is enough
to simply wait for all of the jobs of a particular day to be fully processed before 
running this program.

## Getting Started

### Dependencies

* pandas version(2.2.3)
* numpy version(1.26.4)
* openpyxl version(3.1.3)
* WSL (Windows Subsystem For Linux) or any other linux distribution

### Installing manually

Example running on Linux...

* pip will need to be ran for installing any dependencies in the requirements.txt file

```bash
# in the main project folder as the working directory
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
deactivate
```

### Executing program manually
* The program needs to be executed in the main project folder
* The program also needs it's virtual environment activated
* Finally run the program by main.py from the main project folder

Example running on Linux...

```bash
# in the main project folder as the working directory
source venv/bin/activate
python main.py
deactivate
```
### Authors

Max Kranker (<max.kranker@colecarbide.com>)

## Version History

* 0.1
  * Initial Release

## License

This project is licensed under the MIT License - see the License.md file for details
