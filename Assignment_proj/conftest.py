import inspect
import json
import os
import pytest
from pytest import fixture
from data.testdata import Testdata


temp_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
positive_json_path = os.path.join(temp_dir, 'data', 'test_data.json')
negative_json_path = os.path.join(temp_dir, 'data', 'test_data_negative.json')


@pytest.fixture
def base_url():
    return "https://www.alphavantage.co/query"


@pytest.fixture(params=[Testdata.IBM_DATA_DAILY_COMPACT,
                        Testdata.TESCO_DAILY_COMPACT,
                        Testdata.SHOPIFY_DAILY_COMPACT,
                        Testdata.GREENPWR_DAILY_COMPACT,
                        Testdata.DAIMLER_DAILY_COMPACT])
def data(request):
    return request.param


def load_json(path):
    with open(path) as my_data:
        data = json.load(my_data)
        return data


@fixture(params=load_json(positive_json_path))
def get_positive_data(request):
    positive_data = request.param
    yield positive_data


@fixture(params=load_json(negative_json_path))
def get_negative_data(request):
    negative_data = request.param
    yield negative_data
