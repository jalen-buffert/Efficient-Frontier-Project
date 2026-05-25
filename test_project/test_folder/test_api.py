import pytest
import responses
from unittest import TestCase
from api import CallApi
from requests import RequestException

class TestAPIInit(TestCase):
    #Api.py -
    #CallApi __init__
    def test_initial_api_obj(self):
        from api import CallApi
        api_obj = CallApi(['AAPL','TSLA','MSFT'])
        self.assertEqual(api_obj.needed_tickers, ['AAPL','TSLA','MSFT'])

    def test_no_needed_tickers(self):
        from api import CallApi
        api_obj = CallApi([])
        self.assertEqual(api_obj.needed_tickers, None)

class TestRetrievingJsonData(TestCase):

    def setUp(self):
        from test_folder import api_key
        self.api_key = api_key
    #get_data
    #need to test grabbing 1 ticker
    @responses.activate
    def test_call_api_for_1_ticker(self):
        from api import CallApi
        from fake_data import FakeData

        fd_1 = FakeData(['AAPL'])
        api_1 = fd_1.get_data()
        api_obj = CallApi(['AAPL'])

        responses.add(
            responses.GET,f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={'AAPL'}&apikey={self.api_key}",
            json=api_1['AAPL'][0],
            status=200
        )
        self.assertEqual(api_obj.get_data(), {'AAPL': api_1['AAPL']})

    #Grabbing mutliple tickers
    @responses.activate
    def test_call_api_multi_t(self):
        from api import CallApi
        from fake_data import FakeData

        fd_2 = FakeData(['AAPL','TSLA','MSFT'])
        api_2 = fd_2.get_data()
        api_obj_2 = CallApi(['AAPL','TSLA','MSFT'])

        for ticker in fd_2.tickers_n:
            responses.add(
                responses.GET, f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={ticker}&apikey={self.api_key}",
                json=api_2[ticker][0],
                status=200
            )
        self.assertEqual(api_obj_2.get_data(), {'AAPL': api_2['AAPL'], 'TSLA': api_2['TSLA'], 'MSFT': api_2['MSFT']})

    #Test getting Errors on first ticker of list of singular ticker
    @responses.activate
    def test_RequestException_1_ticker(self):
        from api import CallApi

        api_obj_3 = CallApi(['AAPL'])

        responses.add(
            responses.GET, f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={'AAPL'}&apikey={self.api_key}",
            body=RequestException()
        )
        self.assertEqual(api_obj_3.get_data(),'Error1')

    #Test getting Error1 on second ticker
    @responses.activate
    def test_getting_error_on_2nd_ticker_multi_tickers(self):
        from api import CallApi
        from fake_data import FakeData

        fd_3 = FakeData(['AAPL','TSLA','MSFT','AMD'])
        api_3 = fd_3.get_data()
        api_obj_4 = CallApi(['AAPL','TSLA','MSFT','AMD'])

        responses.add(
            responses.GET,f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={'AAPL'}&apikey={self.api_key}",
            json=api_3['AAPL'][0],
            status=200
        )
        responses.add(
            responses.GET,f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={'TSLA'}&apikey={self.api_key}",
            body=RequestException(),
        )
        self.assertEqual(api_obj_4.get_data(),'Error1')

    #Test getting error on last ticker in list
    @responses.activate
    def test_getting_error_on_last_ticker_multi_tickers(self):
        from api import CallApi
        from fake_data import FakeData

        fd_4 = FakeData(['AAPL','TSLA','MSFT','AMD'])
        api_4 = fd_4.get_data()
        api_obj_5 = CallApi(['AAPL','TSLA','MSFT','AMD'])

        for ticker in fd_4.tickers_n[:-1]:
            responses.add(
                responses.GET,f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={ticker}&apikey={self.api_key}",
                json=api_4[ticker][0],
                status=200
            )
        responses.add(
            responses.GET,f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={'AMD'}&apikey={self.api_key}",
            body=RequestException(),
        )
        self.assertEqual(api_obj_5.get_data(), 'Error1')


    # Testing rate limit Error message
    @responses.activate
    def test_error2_on_1_ticker(self):
        from api import CallApi

        api_obj_6 = CallApi(['AAPL'])

        responses.add(
            responses.GET,f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={'AAPL'}&apikey={self.api_key}",
            #Not what it actually says
            json={'AAPL':' you have reached a rate limit'},
        )

        self.assertEqual(api_obj_6.get_data(), 'Error2')
    #Test rate limit on multiple tickers
    @responses.activate
    def test_error2_on_multi_tickers(self):
        from api import CallApi
        from fake_data import FakeData

        fd_5 = FakeData(['AAPL','TSLA','MSFT','AMD'])
        api_5= fd_5.get_data()
        api_obj_7 = CallApi(['AAPL','TSLA','MSFT','AMD'])

        responses.add(
            responses.GET,f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={'AAPL'}&apikey={self.api_key}",
            json=api_5['AAPL'][0],
            status=200
        )
        responses.add(
            responses.GET,f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={'TSLA'}&apikey={self.api_key}",
            json=api_5['TSLA'][0],
            status=200
        )
        responses.add(
            responses.GET,f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={'MSFT'}&apikey={self.api_key}",
            json={'MSFT':' you have reached a rate limit'},
        )
        self.assertEqual(api_obj_7.get_data(), 'Error2')

class TestRiskFree(TestCase):

    def setUp(self):
        from test_folder import api_key
        self.api_key = api_key

    #Test for retrieving risk free rate
    @responses.activate
    def test_retrieve_risk_free(self):
        from api import CallApi
        from fake_data import FakeData

        fd_6 = FakeData(['AAPL','TSLA'])
        api_6 = fd_6.get_risk_free()
        api_obj_8 = CallApi(['AAPL','TSLA'])

        responses.add(
            responses.GET, f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey={self.api_key}',
            json=api_6,
            status=200
        )
        self.assertEqual(api_obj_8.get_risk_free(), (0.0432,'2026-04-01'))

