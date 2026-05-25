from os import path, getenv
from sys import exit
from pandas import read_csv, to_datetime, DataFrame, isna, Series
from datetime import date

API_KEY = getenv("STOCK_API_KEY1")

#Class that gets the all of the stock data
class RawData:
    def __init__(self, tickers):
        #Make sure the user inputs at least 1 ticker
        if not len(tickers) > 0:
            exit("No tickers entered")
        self.tickers = tickers

    def get_csv(self):
        if path.exists('data.csv'):
            df = read_csv('data.csv')
            df.set_index('Date', inplace=True)
            df.index = to_datetime(df.index)
            df = self.drop_unwanted(df)
        else:
             return DataFrame()
        return df

    #Keep only the data of the user inputted tickers
    def drop_unwanted(self, df):
        common_ticks = [ticker for ticker in df.columns if str(ticker).upper().strip() in str(self.tickers).upper().strip()]
        return df[common_ticks]

    #Gets all of the tickers that are not already in the csv file.
    def update_tickers(self, df):
        this_month, last_month = get_months(get_todays_date())

        tickers_to_update = []
        #Return a list of the tickers in Uppercase and stripped of whitespace
        stock_names = df.columns

        for t in self.tickers:
            name = str(t).upper().strip()
            #Check if user inputted tickers already in the df are updated to the current month..
            # If not we add them to the list of tickers to get.
            if name in stock_names:
                latest_date = str(to_datetime(df.index).max())

                if latest_date == 'NaT':
                    tickers_to_update.append(name)
                    continue
                else:
                    m = int(extract_month(latest_date))
                if not m == last_month and not m == this_month or isna(df[name].iloc[0]):
                    tickers_to_update.append(name)
            else:
                #If the ticker is not in the csv already we also add it to the list to get.
                tickers_to_update.append(name)

        if len(tickers_to_update) == 0:
            return None
        return tickers_to_update

    def parse_data(self, data):
        dates_n_prices = {}
        for ticker in data:
            dict_stock = data[ticker]
            dates_n_prices[ticker] = []
            for date in dict_stock[0]['Monthly Time Series']:
                price = dict_stock[0]['Monthly Time Series'][date]['4. close']
                dates_n_prices[ticker].append((date,price))
        return dates_n_prices

    def dates_of_multiple_tickers(self, dates_and_prices):
        date_list = {}
        for ticker in dates_and_prices:
            if len(dates_and_prices) > 1:
                date_list[ticker] = set()
                date_list[ticker] = set(stock[0] for stock in dates_and_prices[ticker])
            else:
                return dates_and_prices
        return date_list

    def common_dates(self, date_sets):
        try:
            return sorted(set.intersection(*date_sets.values()))
        except:
            return sets

    def merge_data(self, pars_d, comm_dates):
        fin_dict = {}
        for ticker, dateprice in pars_d.items():
            fin_dict[ticker] = []
            merged_data = []
            for val in dateprice:
                merged_data.append([(val[0], val[1]) for date in comm_dates if date == val[0]])

            for stock in merged_data:
                if stock:
                    fin_dict[ticker].append(stock[0])
        return fin_dict

    def to_df(self, data_in_dict):
        df2 = DataFrame()
        df = DataFrame(data_in_dict)
        #Add the date and close prices to the columns
        for col in df:
            df2[['Date',col]]= df[col.upper()].apply(Series)
        #Turn date column into index then drop the date column
        df2.index = df2['Date']
        df2 = df2.drop(columns=['Date'])
        df2.index = to_datetime(df2.index)
        return df2

    def update_df(self, original_df, new_df):
        if original_df.empty:
            return new_df
        fin_dates = [date for date in original_df.index if date in new_df.index]
        original_df = original_df.reindex(fin_dates)
        new_df = new_df.reindex(fin_dates)

        fin_df = original_df.copy()

        for col in new_df.columns:
            fin_df[col] = new_df[col]

        return fin_df

    def to_csv(self, df):
        df.to_csv('data.csv', mode='w')

    @property
    def new_tickers(self):
        return self._new_tickers

    @new_tickers.setter
    def new_tickers(self, new_tickers):
        self._new_tickers = new_tickers

    @property
    def tickers(self):
        return self._tickers

    @tickers.setter
    def tickers(self, tickers):
        self._tickers = tickers

def extract_month(date):
        before_m = date.find('-')
        return date[before_m+1:before_m+3]

def get_todays_date():
     return str(date.today())

def get_months(todays_d):
        today = str(todays_d)
        t_month = int(extract_month(today))

        if not t_month == 1:
            l_month = t_month - 1
        else:
            l_month = 12
        return (t_month,l_month)
