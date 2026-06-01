import pytest
import responses
from os import getenv
from pandas import DataFrame, to_datetime, DatetimeIndex
from main import get_tickers
from api import CallApi
from portfolio import get_stats, calc_returns, annual_metrics, sharpes_r
from unittest.mock import patch, Mock
from data import extract_month, get_months
from datetime import datetime
from unittest import TestCase

#Test any functions created in Main.py


class TestGetTickers(TestCase):

    #Testing get_itckers in main.py
    #Test inputting aapl, tesla, then ctrl d
    @patch('builtins.input', side_effect=['aapl','tsla',EOFError()])
    def test_getticks(self, mock_input):
        self.assertEqual(get_tickers(), ['aapl', 'tsla'])

    #Test inputting mixed upper and lower aapl, tesla...... then ctrl d(exit)
    @patch('builtins.input', side_effect=['aaPl','tSla','AMD','PLtr','msft',EOFError()])
    def test_getmanytickers_upper_and_lower(self, mock_input):
        self.assertEqual(get_tickers(), ['aaPl','tSla','AMD','PLtr','msft'])

    #Test inputting 1 lower ticker then exit
    @patch('builtins.input', side_effect=['aapl', EOFError()])
    def test_getticker(self, mock_input):
        self.assertEqual(get_tickers(), ['aapl'])

    #Test inputting no tickers
    @patch('builtins.input', side_effect=[EOFError()])
    def test_getnotickers(self, mock_input):
        self.assertEqual(get_tickers(), [])


