from requests import get, RequestException
from re import search
from os import getenv, path
from time import sleep
from fetch_data_interface import InformalDataFetchingInterface
from csv import DictWriter, DictReader
from data import extract_month, get_todays_date, get_months

api_Key = getenv("STOCK_API_KEY1")

class CallApi(InformalDataFetchingInterface):
    def __init__ (self, needed_tickers = None):
        if needed_tickers:
            self.needed_tickers = needed_tickers
        else:
            self.needed_tickers = None

    def get_data(self):
        stock_data = {}
        l = 'rate limit'
        #If the list of missing tickers exists we get the data for the tickers in that list
        if self.needed_tickers:
            for stock in self.needed_tickers:
                stock_data[stock] = []
                try:
                    #API KEY should be called here from a variable that gets your API... Dont hardcode in this file
                    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={stock}&apikey={api_Key}'
                    r = get(url)
                    r.raise_for_status()
                except RequestException:
                    return 'Error1'

                ticker_data = r.json()

                match = search(l, str(ticker_data))
                if match:
                    return 'Error2'
                stock_data[stock].append(ticker_data)
                sleep(2)
            return stock_data

    def get_risk_free(self):
        url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey={api_Key}'
        r = get(url)
        data = r.json()

        date = data['data'][0]['date']
        rate = float(data['data'][0]['value'])
        return rate*.01, date

    def to_csv(self, rate):
       with open('risk_free.csv', 'w') as csvfile:
           fieldnames = ['Date','Rate']
           writer = DictWriter(csvfile, fieldnames=fieldnames)
           writer.writeheader()
           writer.writerow({'Date': rate[1],'Rate': rate[0]})

    def read_csv(self,csv):
        with open(csv) as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                return row

    def get_rf_csv(self):
        if path.exists('risk_free.csv'):
            rf = self.read_csv('risk_free.csv')
            if self.is_valid_month(rf['Date']):
                return float(rf['Rate'])
            else:
                new_rf = self.get_risk_free()
                self.to_csv(new_rf)
                return new_rf[0]
        else:
            rf = self.get_risk_free()
            self.to_csv(rf)
            return rf[0]

    def is_valid_month(self,csv_date):
        date = get_todays_date()
        this_month = int(extract_month(date))
        csv_month = int(extract_month(csv_date))
        if this_month == csv_month + 1:
            return True
        else:
            return False

    @property
    def needed_tickers(self):
        return self._needed_tickers

    @needed_tickers.setter
    def needed_tickers(self, needed_tickers):
        self._needed_tickers = needed_tickers

