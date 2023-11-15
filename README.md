# Boiler Plate
Note : Used [this](https://dev.to/nagatodev/getting-started-with-flask-1kn1) tutorial to created this boilerplate - and made my own adjustments.

### Prior to Setup
Ensure you have:
- [Git](https://git-scm.com/download/win) downloadeded and setup on your computer. ```git -v``` in terminal to check.
- [Python 3.X](https://www.python.org/downloads/) downloaded and setup on your computer. `py --version` or `python --version` or `python3 --version` in terminal to check. I am using `python` for the commands in this doc, so if that doesnt work replace it with the one that works for you.
- [PIP 3](https://pip.pypa.io/en/stable/installation/) downloaded and setup. This may come preinstalled with python. To check, run `pip -V`. `python -m pip -V` might also work, but to install the required packages we're using a .bat file and that file uses `pip`, so you may have to create an alias or edit that file.

### Usage

#### First Time:
1. Clone this git: `git clone https://github.com/rgreenan55/SeniorDesign2023BE.git`
2. Move into the directory: `cd SeniorDesign2023BE`
3. Create a Virtual Environment: `python -m venv venv`
4. Load the venv: `.\venv\Scripts\activate`
5. Install all the packages: `.\install_packages.bat` **IMPORTANT! IF YOU INSTALL OTHER PACKAGES ADD THEM TO THIS FILE**
6. Move into the src directory: `cd src`
7. Run the server: `flask run` or `python app.py` (running the second command runs it in debug mode, so it will restart every time a file is changed)

#### Other Times:
1. Move into the main directory: `cd SeniorDesign2023BE`
2. Load the venv: `.\venv\Scripts\activate`
3. Ensure you have all the packages: `.\install_packages.bat` **IMPORTANT! IF YOU INSTALL OTHER PACKAGES ADD THEM TO THIS FILE**
4. Move into the src directory: `cd src`
5. Run the server: `flask run` or `python app.py` (running the second command runs it in debug mode, so it will restart every time a file is changed)