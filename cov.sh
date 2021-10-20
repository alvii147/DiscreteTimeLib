#!/usr/bin/bash

# move to script directory
cd "$(dirname "$0")"

# set PYTHONPATH
export PYTHONPATH=$PWD

# run all tests with coverage
coverage run --source DiscreteTimeLib -m pytest -v -s tests/

# get coverage report
coverage report -m

# erase coverage
coverage erase