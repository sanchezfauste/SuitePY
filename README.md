[![license](https://img.shields.io/github/license/sanchezfauste/SuitePY.svg?style=flat-square)](LICENSE)
[![readthedocs](https://readthedocs.org/projects/suitepy/badge/?version=latest&style=flat-square)](https://suitepy.readthedocs.io/en/latest/)
[![GitHub (pre-)release](https://img.shields.io/github/release/sanchezfauste/SuitePY/all.svg?style=flat-square)](https://github.com/sanchezfauste/SuitePY/releases/latest)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7e38151ed08e483a9c0bb8dc3ce339e0)](https://www.codacy.com/app/sanchezfauste/SuitePY?utm_source=github.com&utm_medium=referral&utm_content=sanchezfauste/SuitePY&utm_campaign=Badge_Grade)

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

## PDF Templates support
To be able to use get_pdf_template method, you need to install a custom WebService on your SuiteCRM instance:

1. Download zip of [latest SuitePY-service release](https://github.com/sanchezfauste/SuitePY-service/releases/latest) and install it using Module Loader.
2. Edit `suitepy.ini` config file and change the `url` parameter to `https://crm.example.com/custom/service/suitepy/rest.php`.
