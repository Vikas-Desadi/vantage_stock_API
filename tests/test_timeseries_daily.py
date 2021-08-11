import pytest
from constants import FUNCTION_ERROR, SYMBOL_ERROR, Information, Time_Zone
from data.testdata import Testdata
from datetime import datetime, timedelta
from tests.common import hit_daily_url


class TestTimeSeriesDaily():
    # writing docstring to only one testcase

    @pytest.mark.health
    def test_health_timeseriesdaily(self, base_url, get_positive_data):
        """
        Test Description:
        This test is to verify the health of an DAILY api

        Test Steps:
        1. Hit the url with GET method with all mandatory query params

        Expected Result:
        1. The status code is "200" in the response
        """
        # res = requests.get(base_url, get_positive_data)
        res = hit_daily_url(base_url, get_positive_data)
        assert res.status_code == 200, "Bad status code"

    # this test is to verify the "Meta Data" object in the response
    @pytest.mark.regression
    def test_metadata_obj(self, base_url, get_positive_data):
        try:
            res = hit_daily_url(base_url, get_positive_data)
            # if 'API call frequency is 5 calls per minute' in res.text:
            #     time.sleep(SLEEP_FOR)
            response_json = res.json()
            assert res.status_code == 200, "Bad status code"
            # verifying the "1. Information" attribute in the response as expected
            assert response_json['Meta Data']['1. Information'] == Information
            # verifying the "2. Symbol" attribute is same as what is in the
            # json request
            assert get_positive_data['symbol'] == response_json['Meta Data'][
                '2. Symbol']
            # verifying the "4. Output Size" attribute in the response as expected
            assert get_positive_data['outputsize'] == \
                   response_json['Meta Data']['4. Output Size']
            # verifying the "5. Time Zone" attribute in the response as expected
            assert response_json['Meta Data']['5. Time Zone'] == Time_Zone
        except KeyError as e:
            print("Key Error in response: ", e)


    # this test is to verify the "Last Refreshed" attribute in the response
    @pytest.mark.regression
    def test_metadata_lastrefreshed(self, base_url, get_positive_data):
        try:
            res = hit_daily_url(base_url, get_positive_data)
            response_json = res.json()
            current_time = datetime.now().strftime("%H:%M:%S")
            time_now = current_time.split(":")[0]
            today_date = datetime.today().strftime('%Y-%m-%d')
            yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
            day_before = (datetime.today() - timedelta(days=2)).strftime(
                '%Y-%m-%d')
            two_day_before = (datetime.today() - timedelta(days=3)).strftime(
                '%Y-%m-%d')
            weekno = datetime.today().weekday()
            # if the day is saturday then "Last Refreshed" should reflect
            # yesterday's date of execution date
            if weekno == 5:
                assert yesterday == response_json['Meta Data']['3. Last Refreshed']
            # if the day is sunday then "Last Refreshed" should reflect
            # day before yesterday's date of execution date
            elif weekno == 6:
                assert day_before == response_json['Meta Data'][
                    '3. Last Refreshed']
            # if the day is monday and the local time is less than 10 am EST
            # then "Last Refreshed" should reflect three days before the date
            # of execution date
            elif weekno == 0 and time_now <= '19':
                assert two_day_before == response_json['Meta Data'][
                    '3. Last Refreshed']
            else:
                # if the day is weekday then "Last Refreshed" should reflect
                # today's date
                assert today_date == response_json['Meta Data'][
                    '3. Last Refreshed']
        except KeyError as e:
            print("Key Error in response: ", e)


    # this test is to verify the "Time Series (Daily)" object in the response
    @pytest.mark.regression
    def test_timeseriesdaily_obj(self, base_url, data):
        try:
            res = hit_daily_url(base_url, data)
            assert res.status_code == 200, "Bad status code"
            response_json = res.json()
            # all the attributes of the "Time Series (Daily)" object should be str
            for item in response_json['Time Series (Daily)']:
                assert type(response_json['Time Series (Daily)'][item][
                                '1. open']) is str, "Fail, bad element type"
                assert type(response_json['Time Series (Daily)'][item][
                                '2. high']) is str, "Fail, bad element type"
                assert type(response_json['Time Series (Daily)'][item][
                                '3. low']) is str, "Fail, bad element type"
                assert type(response_json['Time Series (Daily)'][item][
                                '4. close']) is str, "Fail, bad element type"
                assert type(response_json['Time Series (Daily)'][item][
                                '5. volume']) is str, "Fail, bad element type"
        except KeyError as e:
            print("Key Error in response: ", e)

    # this test is to verify the neagtive scenarios of the API
    @pytest.mark.regression
    def test_negative_api(self, base_url, get_negative_data):
        try:
            res = hit_daily_url(base_url, get_negative_data)
            # the url is hit with the null "function" quesry param and failure
            # is expected
            if get_negative_data["function"] == "":
                assert FUNCTION_ERROR in res.text, "Failure is expected"
                # the url is hit with the null "symbol" quesry param and failure
                # is expected
            elif get_negative_data["symbol"] == "":
                assert SYMBOL_ERROR in res.text, "Failure is expected"
        except KeyError as e:
            print("Key Error in response: ", e)


    # This is used just in case of doing with marker parameterization
    @pytest.mark.parametrize(
        ("test_data", "symbol"), [(Testdata.IBM_DATA_DAILY_COMPACT, "IBM"),
                                  (Testdata.TESCO_DAILY_COMPACT, "TSCO.LON"),
                                  (Testdata.SHOPIFY_DAILY_COMPACT, "SHOP.TRT"),
                                  (Testdata.GREENPWR_DAILY_COMPACT, "GPV.TRV"),
                                  (Testdata.DAIMLER_DAILY_COMPACT, "DAI.DEX")])
    def test_IBM_stats(self, base_url, test_data, symbol):
        try:
            res = hit_daily_url(base_url, test_data)
            assert res.status_code == 200, "Bad status code"
            response_json = res.json()
            assert response_json['Meta Data'][
                       '2. Symbol'] == symbol, "Symbol is not correct"
        except KeyError as e:
            print("Key Error in response: ", e)

