#!/bin/bash


python3 -m venv venv

source venv/bin/activate

pip install Flask
pip install flask_sqlalchemy
pip install mysql-connector-python
pip install requests
