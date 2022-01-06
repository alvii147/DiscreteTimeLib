# move to script parent directory
cd "$(dirname "$0")"

# set PYTHONPATH
export PYTHONPATH=${PWD}

# run all tests with coverage
coverage run -m pytest -v -s tests/

# get coverage report
coverage report
code=$?

# erase coverage
coverage erase

exit $code
