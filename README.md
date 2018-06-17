[![readthedocs](https://readthedocs.org/projects/suitepy/badge/?version=latest&style=flat-square)](https://suitepy.readthedocs.io/en/latest/)
[![GitHub (pre-)release](https://img.shields.io/github/release/sanchezfauste/SuitePY/all.svg?style=flat-square)](https://github.com/sanchezfauste/SuitePY/releases/latest)

# SuitePY

Suite PY is a simple Python client for SuiteCRM API.

## How to prepare the environment on Linux (Debian)
In this section is described how to get the development environment ready on Debian based systems.

It's recommended to use `virtualenv` and `pip` packages. You can install this two dependencies runnig:
```bash
sudo apt-get update
sudo apt-get install virtualenv python-pip
```

Once you have `virtualenv` and `pip` tools ready it's time to prepare the virtual environment to run the application.  
Following we create a virtual environment and install all Python dependencies:
```bash
cd SuitePY
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
