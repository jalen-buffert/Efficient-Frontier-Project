from unittest import TestCase
from pandas import DataFrame
from portfolio import get_stats, calc_returns, annual_metrics, sharpes_r, optimal_port, random_ports
import math

class TestMetrics(TestCase):

    #Test computing the returns
    def test_calc_returns(self):
        df = DataFrame(data = {'AAPL':['13.50','12.00','10.0'],'TSLA': ['10.00','7.00','5.00']}, index = ['2026-04-15','2026-03-31','2026-03-16'])
        self.assertTrue(calc_returns(df).equals(DataFrame(data = {'AAPL': [0.20, 0.125], 'TSLA': [0.40,0.4286]}, index= ['2026-03-31','2026-04-15'])))

    #Test returns being negative
    def test_calc_returns2(self):
        df = DataFrame(data = {'AAPL':['100.0','120.00','115.0'],'TSLA': ['65.00','70.00','71.00']}, index = ['2026-04-15','2026-03-31','2026-03-16'])
        self.assertTrue(calc_returns(df).equals(DataFrame(data = {'AAPL': [0.0435, -0.1667], 'TSLA': [-0.0141,-0.0714]}, index= ['2026-03-31','2026-04-15'])))

    #Test returns being 0
    def test_no_returns(self):
        df = DataFrame(data = {'AAPL':['100.0','100.00','100.0'],'TSLA': ['200.00','200.00','200.00']}, index = ['2026-04-15','2026-03-31','2026-03-16'])
        self.assertTrue(calc_returns(df).equals(DataFrame(data = {'AAPL': [0.0, 0.0], 'TSLA': [0.0,0.0]}, index= ['2026-03-31','2026-04-15'])))

    #get_stats
    #testing if if the descriptive stats and adding transposed variance
    def test_get_stats(self):
        df = DataFrame(data = {'AAPL':['20.0','15.00','10.0','5.0'],'TSLA': ['10.00','6.00','3.00','1.00']}, index = ['2026-04-15','2026-03-31','2026-03-16','2026-03-10'])
        df2 = DataFrame(data ={'AAPL': {'count': 3.000000, 'mean': 0.611100,'std': 0.346958,'min':0.333300,'25%': 0.416650,'50%': 0.500000,'75%': 0.750000,'max': 1.000000,'var': 0.120380},
                'TSLA': {'count': 3.000000, 'mean': 1.222233,'std': 0.693875,'min':0.666700,'25%': 0.833350,'50%': 1.000000,'75%': 1.500000,'max': 2.000000,'var': 0.481463}
        })
        self.assertTrue(get_stats(calc_returns(df)).equals(df2))
    #annual_metrics
    def test_annual_metrics(self):
        df = DataFrame(data = {'AAPL':['20.0','15.00','10.0','5.0'],'TSLA': ['10.00','6.00','3.00','1.00']}, index = ['2026-04-15','2026-03-31','2026-03-16','2026-03-10'])
        stats = get_stats(calc_returns(df))
        self.assertEqual(annual_metrics(stats), [('AAPL', 0.6111, 304.822879,1.201898), ('TSLA', 1.222233, 14502.576519, 2.403654)])

    #annual Sharpe Ratio
    def test_ann_sharpe(self):
        df = DataFrame(data = {'AAPL':['8.7','7.0','6.5','5.0'],'TSLA': ['107.00','104.2','99.7','100.00']}, index = ['2026-04-15','2026-03-31','2026-03-16','2026-03-10'])
        ann = annual_metrics(get_stats(calc_returns(df)))
        self.assertEqual(sharpes_r(ann), [('AAPL', 8.415089982783357), ('TSLA', -0.1997631294084085)])


class TestOptimalPortfolio(TestCase):

    def setUp(self):
        self.returns = calc_returns(DataFrame(data = {'AAPL':['20.0','15.00','10.0','5.0'],'TSLA': ['10.00','6.00','3.00','1.00']}, index = ['2026-04-15','2026-03-31','2026-03-16','2026-03-10']))
        self.optimal_portfolio = optimal_port(self.returns)
        self.periods = 12

    def test_num_portfolios(self):
        self.assertEqual(len(self.optimal_portfolio['Returns']),150)

    def test_float_values(self):
        for category in self.optimal_portfolio:
            if category != 'Min_Var_P':
                types_are_float =  all(isinstance(port, float) for port in self.optimal_portfolio[category])
        self.assertTrue(types_are_float)

    def test_nan_values(self):
        for item in self.optimal_portfolio:
            if item != 'Min_Var_P':
                no_nans = all(not math.isnan(port) for port in self.optimal_portfolio[item])
        self.assertTrue(no_nans)

    def test_non_neg_vol(self):
        positive_vols = all(vol > 0 for vol in self.optimal_portfolio['Volatility'])
        self.assertTrue(positive_vols)

    def test_categories(self):
        keys = [category for category in self.optimal_portfolio]
        self.assertEqual(keys, ['Returns', 'Volatility', 'Sharpes Ratio','Min_Var_P'])

    def test_min_var_port(self):
        min_var_return = self.optimal_portfolio['Returns'][0]
        self.assertTrue(math.isclose(min_var_return,self.optimal_portfolio['Min_Var_P']))

    def test_max_return(self):
        max_return = self.optimal_portfolio['Returns'][-1]
        self.assertTrue(math.isclose(max_return,max(self.returns.mean() * self.periods),rel_tol=0.0001))

class TestRandomPorts(TestCase):
    def setUp(self):
        self.returns = calc_returns(DataFrame(data = {'AAPL':['20.0','15.00','10.0','5.0'],'TSLA': ['10.00','6.00','3.00','1.00']}, index = ['2026-04-15','2026-03-31','2026-03-16','2026-03-10']))
        self.random_port = random_ports(self.returns)

    def test_categories(self):
        keys = [category for category in self.random_port]
        self.assertEqual(keys, ['Returns','Volatility','AAPL weight','TSLA weight','Sharpe'])

    def test_no_nan(self):
        for item in self.random_port:
            no_nans = all(not math.isnan(port) for port in self.random_port[item])
        self.assertTrue(no_nans)

    def test_all_floats(self):
        for category in self.random_port:
            all_floats = all(isinstance(port,float) for port in self.random_port[category])
        self.assertTrue(all_floats)

    def test_all_positive(self):
        for category in self.random_port:
            all_positive = all(value > 0 for value in self.random_port[category])
        self.assertTrue(all_positive)

    def test_num_ports(self):
        n_samples = 5000
        self.assertEqual(len(self.random_port),n_samples)
    #random_ports

