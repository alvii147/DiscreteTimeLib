#!/usr/bin/bash

# move to script directory
cd "$(dirname "$0")"

# set PYTHONPATH
export PYTHONPATH=$PWD

# run all tests
coverage run --source DiscreteTimeLib -m pytest -v

# get coverage report
coverage report -m

# erase coverage
coverage erase