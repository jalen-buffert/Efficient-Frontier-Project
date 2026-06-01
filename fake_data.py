from fetch_data_interface import InformalDataFetchingInterface

class FakeData(InformalDataFetchingInterface):
    def __init__ (self, tickers_n =None):
        if tickers_n:
            self.tickers_n = tickers_n
        else:
            self.tickers_n = None

    def get_data(self):
        dict = {}

        fake_ticker_data = [[{'Meta Data': {'1. Information': 'Monthly Prices (open, high, low, close) and Volumes',
                            '2. Symbol': '', '3. Last Refreshed': '2026-04-15', '4. Time Zone': 'US/Eastern'},'Monthly Time Series':
                            {'2026-04-15':{'1. open': '254.0800', '2. high': '266.5600','3. low': '245.7000', '4. close': '2.0', '5. volume': '397791457'},
                            '2026-03-31': {'1. open': '262.4100', '2. high': '266.5300', '3. low': '245.5100', '4. close': '3.0', '5. volume': '900035757'}}}],
                            [{'Meta Data': {'1. Information': 'Monthly Prices (open, high, low, close) and Volumes',
                            '2. Symbol': '', '3. Last Refreshed': '2026-04-15', '4. Time Zone': 'US/Eastern'},'Monthly Time Series':
                            {'2026-04-15':{'1. open': '254.0800', '2. high': '266.5600','3. low': '245.7000', '4. close': '2.0', '5. volume': '397791457'},
                            '2026-03-31': {'1. open': '262.4100', '2. high': '266.5300', '3. low': '245.5100', '4. close': '3.0', '5. volume': '900035757'},
                            '2026-02-27': {'1. open': '260.0300', '2. high': '280.9050', '3. low': '255.4500', '4. close': '4.0', '5. volume': '988325816'},}}],
                            [{'Meta Data': {'1. Information': 'Monthly Prices (open, high, low, close) and Volumes',
                            '2. Symbol': '', '3. Last Refreshed': '2026-04-15', '4. Time Zone': 'US/Eastern'},'Monthly Time Series':
                            {'2026-04-15':{'1. open': '254.0800', '2. high': '266.5600','3. low': '245.7000', '4. close': '2.0', '5. volume': '397791457'},
                            '2026-03-31': {'1. open': '262.4100', '2. high': '266.5300', '3. low': '245.5100', '4. close': '3.0', '5. volume': '900035757'},
                            '2026-02-27': {'1. open': '260.0300', '2. high': '280.9050', '3. low': '255.4500', '4. close': '4.0', '5. volume': '988325816'},
                            '2026-01-30': {'1. open': '272.2550', '2. high': '277.8400', '3. low': '243.4200', '4. close': '5.0', '5. volume': '1036170325'}}}],
                            [{'Meta Data': {'1. Information': 'Monthly Prices (open, high, low, close) and Volumes',
                            '2. Symbol': '' , '3. Last Refreshed': '2026-04-15', '4. Time Zone': 'US/Eastern'},'Monthly Time Series':
                            {'2026-04-15':{'1. open': '254.0800', '2. high': '266.5600','3. low': '245.7000', '4. close': '2.0', '5. volume': '397791457'},
                            '2026-03-31': {'1. open': '262.4100', '2. high': '266.5300', '3. low': '245.5100', '4. close': '3.0', '5. volume': '900035757'},
                            '2026-02-27': {'1. open': '260.0300', '2. high': '280.9050', '3. low': '255.4500', '4. close': '4.0', '5. volume': '988325816'},
                            '2026-01-30': {'1. open': '272.2550', '2. high': '277.8400', '3. low': '243.4200', '4. close': '5.0', '5. volume': '1036170325'},
                            '2025-12-31': {'1. open': '278.0100', '2. high': '288.6200', '3. low': '266.9500', '4. close': '6.0', '5. volume': '922283649'}}}]
        ]

        i = 0
        for ticker in self.tickers_n:
            index_d = i % 4
            dict[ticker] = fake_ticker_data[index_d]
            dict[ticker][0]['Meta Data']['Symbol'] = ticker
            i += 1
        return dict


    def get_risk_free(self):
        return {'name': '10-Year Treasury Constant Maturity Rate', 'interval': 'monthly', 'unit': 'percent', 'data': [{'date': '2026-04-01', 'value': '4.32'},
                                                                                                                      {'date': '2026-04-02', 'value': '4.32'}]}

    @property
    def tickers_n(self):
        return self._tickers_n
    @tickers_n.setter
    def tickers_n(self, tickers):
        self._tickers_n = tickers


