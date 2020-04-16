#!/bin/bash

virtualenv venv
source venv/bin/activate

# install project's requirements

python -m pip install -r requirements.txt

# install the project
python -m pip install .

# create .env file from the sample
cp sample.env .env

echo "Remember to set your env variables in the .env file."

echo "Congrats! You are ready to go"