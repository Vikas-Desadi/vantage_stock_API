# Building an API test automation framework with Python


Ensure you have pipenv already installed:

# Setup
1.Clone git repository

2.Go in a project folder

# Install the required package
pip install -r requirements.txt

You can either use your IDE or terminal to switch to that branch and see the last updated commit.

How to run
got to tests folder

# Run tests via pytest
python -m pytest


# Report results to report portal
pytest -s -v test_timeseries_daily.py --html==reports/report.html
