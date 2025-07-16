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
* WSL (Windows Subsystem For Linux) Unsure if this program can just run locally on Windows

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program
* The program needs to be executed in the main project folder
* The program also needs it's virtual environment activated
* pip will need to be ran for installing any dependencies in the
requirements.txt file

Example running on Linux...

```bash
# in the main project folder as the working directory
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

Example running in windows powershell...
```powercode
python -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
deactivate
```

* Finally run the program by main.py from the main project folder
Example running on Linux...

```bash
# in the main project folder as the working directory
source venv/bin/activate
python main.py
deactivate
```

Example running in windows powershell...
```powercode
.\venv\Scripts\activate.ps1
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
