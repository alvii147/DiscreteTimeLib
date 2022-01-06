# move to script directory
cd "$(dirname "$0")"

# run flake8
flake8 DiscreteTimeLib/ --count --show-source --statistics

# run black
black --check --skip-string-normalization DiscreteTimeLib/
