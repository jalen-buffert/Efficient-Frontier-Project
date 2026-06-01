import pytest
from unittest import TestCase
from pandas import DataFrame, DatetimeIndex, to_datetime
from unittest.mock import patch
from data import extract_month, get_months

#Tests for Data.py

class TestDataInit(TestCase):
    #RawData init - inputting no tickers
    def test_raw_data(self):
        from data import RawData
        with pytest.raises(SystemExit):
            tickers=[]
            RawData(tickers)

    #RawData init - inputting multiple tickers
    def test_data_w_tickers(self):
        from data import RawData
        ticker_l = RawData(['aapl','tsla','amd','msft'])
        self.assertEqual(ticker_l.tickers, ['aapl','tsla','amd','msft'])

    #RawData init - inputting 1 ticker
    def test_data_w_1_ticker(self):
        from data import RawData
        ticker_l = RawData(['aapl'])
        self.assertEqual(ticker_l.tickers, ['aapl'])


class TestDroppingTickers(TestCase):
    #Dropping 1 ticker
    def test_dropping_unwanted(self):
        from data import RawData
        user_tickers = RawData(['aapl','tsla','amd'])
        d = {'aapl':[0.34, 0.02], 'amd':[0.14,0.17], 'pltr':[0.23,0.34]}
        df = DataFrame(data=d)
        self.assertEqual(user_tickers.drop_unwanted(df).equals(DataFrame(data={'aapl':[0.34, 0.02], 'amd':[0.14,0.17]})), True)

    #Dropping all tickers
    def test_dropping_all(self):
        from data import RawData
        user_tickers = RawData(['aapl','tsla','amd'])
        d = {'msft':[0.34, 0.02], 'spy':[0.14,0.17], 'pltr':[0.23,0.34]}
        df = DataFrame(data=d)
        self.assertEqual(user_tickers.drop_unwanted(df).equals((DataFrame(data={},index=df.index))), True)

    #Keeping all tickers
    def test_dropping_none(self):
        from data import RawData
        user_tickers = RawData(['msft','spy','pltr'])
        d = {'msft':[0.34, 0.02], 'spy':[0.14,0.17], 'pltr':[0.23,0.34]}
        df = DataFrame(data=d)
        self.assertEqual(user_tickers.drop_unwanted(df).equals((DataFrame(data={'msft':[0.34, 0.02], 'spy':[0.14,0.17], 'pltr':[0.23,0.34]}))), True)


class TestCSV(TestCase):
    #get_csv
    #Mock if 'data.csv' does not exist
    #Needs to return empty df object
    @patch('data.path')
    def test_no_csv(self, mock_os):
        from data import RawData
        data_obj = RawData(['Any_ticker'])
        mock_os.exists.return_value = False

        result = data_obj.get_csv()

        self.assertTrue(result.empty)
        self.assertIsInstance(result, DataFrame)
        mock_os.exists.assert_called_with('data.csv')

    #Mock if 'data.csv' does exist and we want all of the tickers in the csv
    @patch('data.read_csv')
    @patch('data.path')
    def test_retrieving_csv(self, mock_os, mock_csv):
        from data import RawData
        mock_os.exists.return_value = True
        data_obj = RawData(['AAPL','TSLA'])
        d = DataFrame(data = {'Date': ['2025-02-27', '2025-02-28','2025-03-01'], 'AAPL':[254.21, 256.43, 258.53],'TSLA':[155.34,157.45,154.34]})
        mock_csv.return_value = d

        data = data_obj.get_csv()

        self.assertEqual(data.index.name, 'Date')
        self.assertIsInstance(data.index, DatetimeIndex)
        mock_os.exists.assert_called_with('data.csv')


class TestMonthExtraction(TestCase):
    #extract_months
    def test_extraction(self):
        self.assertEqual(extract_month('2020-03-18'), '03')

    #get_months
    #With January as the month
    def test_jan(self):
        self.assertEqual(get_months('2025-01-21'), (0o1,12))

    #With March as the month
    def test_mar(self):
        self.assertEqual(get_months('2018-03-21'), (0o3,0o2))

    #With December as month
    def test_dec(self):
        self.assertEqual(get_months('2015-12-16'), (12,11))

class TestUpdatingTickers(TestCase):

    #update_tickers
    def test_no_updates_needed(self):
        from data import RawData
        data_obj = RawData(['AAPL', 'TSLA'])
        df = DataFrame(data = {'AAPL':[254.21, 256.43, 258.53],'TSLA':[155.34,157.45,154.34]}, index = ['2025-04-27', '2025-04-28','2025-04-01'])
        self.assertEqual(data_obj.update_tickers(df), None)

    def test_no_updates_needed_date_special(self):
        from data import RawData
        data_obj = RawData(['AAPL', 'TSLA'])
        df = DataFrame(data = {'AAPL':[254.21, 256.43, 258.53],'TSLA':[155.34,157.45,154.34]}, index = ['2022-01-27', '2021-03-28','2025-04-01'])
        self.assertEqual(data_obj.update_tickers(df), None)

    def test_all_updates_needed_for_name(self):
        from data import RawData
        data_obj = RawData(['AAPL', 'TSLA'])
        df = DataFrame(data = {'Date': ['2025-04-27', '2025-04-28','2025-04-01'], 'PLTR':[254.21, 256.43, 258.53],'AMD':[155.34,157.45,154.34]})
        self.assertEqual(data_obj.update_tickers(df), ['AAPL','TSLA'])

    def test_all_updates_needed_for_date(self):
        from data import RawData
        data_obj = RawData(['AAPL', 'TSLA'])
        df = DataFrame(data = {'Date': ['2025-12-27', '2025-01-28','2025-02-01'], 'AAPL':[254.21, 256.43, 258.53],'TSLA':[155.34,157.45,154.34]})
        self.assertEqual(data_obj.update_tickers(df), ['AAPL','TSLA'])

    def test_all_updates_needed_for_date2(self):
        from data import RawData
        data_obj = RawData(['AAPL', 'TSLA'])
        df = DataFrame(data = {'Date': ['2024-03-29', '2025-02-24','2025-02-01'], 'AAPL':[254.21, 256.43, 258.53],'TSLA':[155.34,157.45,154.34]})
        self.assertEqual(data_obj.update_tickers(df), ['AAPL','TSLA'])

    def test_update_1_ticker(self):
        from data import RawData
        data_obj = RawData(['AAPL', 'TSLA', 'PLTR'])
        df = DataFrame(data = {'AAPL':[254.21, 256.43, 258.53],'PLTR':[155.34,157.45,154.34]}, index = ['2025-04-27', '2025-04-28','2025-04-01'])
        self.assertEqual(data_obj.update_tickers(df), ['TSLA'])

    def test_update_multiple_tickers(self):
        from data import RawData
        data_obj = RawData(['AAPL', 'TSLA', 'PLTR','MSFT'])
        df = DataFrame(data = {'AAPL':[254.21, 256.43, 258.53],'PLTR':[155.34,157.45,154.34]}, index = ['2025-04-27', '2025-04-28','2025-04-01'])
        self.assertEqual(data_obj.update_tickers(df), ['TSLA','MSFT'])

class TestParseData(TestCase):
    #parse_data
    def test_parsed_data_1_ticker(self):
        from data import RawData
        from fake_data import FakeData
        fd = FakeData(['AAPL'])
        data_1 = fd.get_data()
        data_obj = RawData(['AAPL'])
        self.assertEqual(data_obj.parse_data(data_1), {'AAPL':[('2026-04-15','2.0'),('2026-03-31','3.0')]})

    def test_parsed_data_multi_tickers(self):
        from data import RawData
        from fake_data import FakeData
        data_obj = RawData(['AAPL','TSLA'])
        fd = FakeData(['AAPL','TSLA'])
        data_1 = fd.get_data()
        self.assertEqual(data_obj.parse_data(data_1), {'AAPL':[('2026-04-15','2.0'),('2026-03-31','3.0')],
                                            'TSLA':[('2026-04-15','2.0'),('2026-03-31','3.0'),('2026-02-27','4.0')]
                                                })

class TestForMultipleTickers(TestCase):
    #dates_of_multiple_tickers
    def test_one_ticker(self):
        from data import RawData
        from fake_data import FakeData
        data_obj = RawData(['AAPL'])
        fd = FakeData(['AAPL'])
        fd_data = fd.get_data()
        fake_dates_and_prices = data_obj.parse_data(fd_data)
        self.assertEqual(data_obj.dates_of_multiple_tickers(fake_dates_and_prices), fake_dates_and_prices)

    def test_multiple_tickers(self):
        from data import RawData
        from fake_data import FakeData
        data_obj = RawData(['AAPL','TSLA'])
        fd = FakeData(['AAPL','TSLA'])
        fd_data = fd.get_data()
        fake_dates_and_prices = data_obj.parse_data(fd_data)
        self.assertEqual(data_obj.dates_of_multiple_tickers(fake_dates_and_prices), {'AAPL':{'2026-04-15','2026-03-31'},
                                            'TSLA':{'2026-04-15','2026-03-31','2026-02-27'}
                                                })

    #common_dates
    def test_sorting_dates_with_many_tickers(self):
        from data import RawData
        from fake_data import FakeData
        data_obj = RawData(['AAPL','TSLA','MSFT','AMD'])
        fd = FakeData(['AAPl','TSLA','MSFT','AMD'])
        fd_data = fd.get_data()
        fk_dt_n_p = data_obj.parse_data(fd_data)
        multiple_t = data_obj.dates_of_multiple_tickers(fk_dt_n_p)
        self.assertEqual(data_obj.common_dates(multiple_t), ['2026-03-31','2026-04-15'])

    #merge_data
    def test_merging_multiple_tickers(self):
        from data import RawData
        from fake_data import FakeData
        data_obj = RawData(['AAPL','TSLA'])
        fd = FakeData(['AAPl','TSLA'])
        fd_data = fd.get_data()
        fk_dt_n_p = data_obj.parse_data(fd_data)
        multiple_t = data_obj.dates_of_multiple_tickers(fk_dt_n_p)
        common_d = data_obj.common_dates(multiple_t)

        self.assertEqual(data_obj.merge_data(fk_dt_n_p,common_d), {'AAPl': [('2026-04-15','2.0'),('2026-03-31','3.0')],
                                                        'TSLA': [('2026-04-15','2.0'),('2026-03-31','3.0')]
        })

    def test_merging_more_tickers(self):
        from data import RawData
        from fake_data import FakeData
        data_obj = RawData(['AAPL','TSLA','MSFT','AMD'])
        fd = FakeData(['AAPL','TSLA','MSFT','AMD'])
        fd_data = fd.get_data()
        fk_dt_n_p = data_obj.parse_data(fd_data)
        new_d = fk_dt_n_p.copy()
        new_d.pop('AAPL')

        multiple_t = data_obj.dates_of_multiple_tickers(new_d)
        common_d = data_obj.common_dates(multiple_t)

        self.assertEqual(data_obj.merge_data(new_d,common_d), {'TSLA': [('2026-04-15','2.0'),('2026-03-31','3.0'),('2026-02-27','4.0')],
                                                        'MSFT': [('2026-04-15','2.0'),('2026-03-31','3.0'),('2026-02-27','4.0')],
                                                        'AMD': [('2026-04-15','2.0'),('2026-03-31','3.0'),('2026-02-27','4.0')]
        })

    #to_df
    def test_merged_data_todf(self):
        from data import RawData
        from fake_data import FakeData
        data_obj = RawData(['AAPL','TSLA'])
        fd = FakeData(['AAPL','TSLA'])
        fd_data = fd.get_data()
        fk_dt_n_p = data_obj.parse_data(fd_data)
        multiple_t = data_obj.dates_of_multiple_tickers(fk_dt_n_p)
        common_d = data_obj.common_dates(multiple_t)
        merged_dict = data_obj.merge_data(fk_dt_n_p,common_d)
        df = DataFrame(data = {'AAPL':['2.0','3.0'],'TSLA': ['2.0','3.0']}, index = ['2026-04-15','2026-03-31'])
        df.index.name = 'Date'
        df.index = to_datetime(df.index)
        k = data_obj.to_df(merged_dict)
        print(k,df)
        self.assertTrue(k.equals(df))

    def test_parsed_data_todf(self):
        from data import RawData
        from fake_data import FakeData
        data_obj = RawData(['AAPL','TSLA'])
        fd = FakeData(['AAPL','TSLA'])
        fd_data = fd.get_data()
        fk_dt_n_p = data_obj.parse_data(fd_data)
        multiple_t = data_obj.dates_of_multiple_tickers(fk_dt_n_p)
        common_d = data_obj.common_dates(multiple_t)
        merged_dict = data_obj.merge_data(fk_dt_n_p,common_d)
        df = DataFrame(data = {'AAPL':['2.0','3.0'],'TSLA': ['2.0','3.0']}, index = ['2026-04-15','2026-03-31'])
        df.index.name = 'Date'
        df.index = to_datetime(df.index)
        self.assertTrue(data_obj.to_df(merged_dict).equals(df))

class UpdateDF(TestCase):
    #update_df
    def test_updating_df(self):
        from data import RawData
        data_obj = RawData(['AAPL','TSLA'])
        original_df = DataFrame(data = {'AAPL':['266.4300','253.7900','222.5410','240.0010'],'TSLA': ['266.4300','253.7900','222.5410','240.0010']}, index = ['2026-04-15','2026-03-31','2026-02-24','2026-01-25'])
        new_df = DataFrame(data = {'PLTR':['266.4300','253.7900','222.5410','240.0010'],'MSFT': ['266.4300','253.7900','222.5410','240.0010']}, index = ['2026-04-15','2026-03-31','2026-02-28','2026-01-30'])
        self.assertTrue(data_obj.update_df(original_df,new_df).equals(DataFrame(data = {'AAPL':['266.4300','253.7900'],
                                                                        'TSLA': ['266.4300','253.7900'],
                                                                        'PLTR':['266.4300','253.7900'],
                                                                        'MSFT': ['266.4300','253.7900']},
                                                                index = ['2026-04-15','2026-03-31'])))

