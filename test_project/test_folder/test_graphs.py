from unittest import TestCase
from graphs import efficient_frontier_visual
import pytest
from portfolio import random_ports, calc_returns
from unittest.mock import patch
import graphs
from pandas import DataFrame
from plotly.graph_objects import Figure, Scattergl, Scatter
from plotly import express

class TestGraph(TestCase):

    @patch('graphs.optimal_port')
    def setUp(self, mock_port):
        dict1 = {'Returns':[],'Volatility':[],'Sharpes Ratio':[],'Min_Var_Port':1.544}
        mock_port.return_value = dict1

        returns = calc_returns(DataFrame(data = {'AAPL':['20.0','15.00','10.0','5.0'],
                                                 'TSLA': ['10.00','6.00','3.00','1.00'],
                                                 'MSFT':['35.00','40.35','32.2','31.9']}, index = ['2026-04-15','2026-03-31','2026-03-16','2026-03-10'])
        )

        self.frontier = efficient_frontier_visual(random_ports(returns),returns,show=False)

    def test_plotly_obj(self):
        self.assertTrue(isinstance(self.frontier,Figure))

    def test_num_traces(self):
        self.assertEqual(len(self.frontier.data),2)

    def test_type_trace1(self):
        self.assertTrue(isinstance(self.frontier.data[0],Scattergl))

    def test_type_trace2(self):
        self.assertTrue(isinstance(self.frontier.data[1],Scatter))

    def test_x_axis_title(self):
        self.assertEqual(self.frontier.layout.xaxis.title.text,'Annual Volatility')

    def test_y_axis_title(self):
        self.assertEqual(self.frontier.layout.yaxis.title.text,'Annual Return')

    def test_title(self):
        self.assertEqual(self.frontier.layout.title.text, 'Efficient Frontier')
