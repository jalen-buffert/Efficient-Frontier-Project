from data import RawData
from api import CallApi
import logging
from portfolio import random_ports, calc_returns
from graphs import efficient_frontier_visual


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    #Instantiate RawData Object
    tickers = RawData(get_tickers())
    #Need to get the data from existing csv
    df = tickers.get_csv()
    #Update any data that is outdated or missing
    tickers_to_update = tickers.update_tickers(df)
    fin_df = build_updated_df(tickers, df, tickers_to_update)

    #Update the csv with the new data
    tickers.to_csv(fin_df)

    #Calculate the all values to build and return the efficient frontier.
    print(efficient_frontier(fin_df))


#Allows user to input tickers
def get_tickers():
    t = []
    while True:
        try:
            t.append(input("Ticker: "))
        except:
            break
    return t
def build_updated_df(tickers, df, tickers_to_upd):
    #If there are no tickers to update just return the original df.
    if tickers_to_upd is None:
        final_df = df.copy(deep=True)
        logger.info('Data From CSV - Nothing to Update %s', final_df)
    else:
        #Initiate API Object that will get data for missing tickers
        missing_t = CallApi(tickers_to_upd)
        #Get data for missing tckers
        new_data = missing_t.get_data()
        #If bad api request or rate limiting, throw error
        if new_data == 'Error1':
            print('Bad Request')
            raise ValueError
        elif new_data == 'Error2':
            print('Rate Limit')
            raise ValueError

        #Parse data to extract dates and prices
        parsed_data = tickers.parse_data(new_data)

        #Get dictionaries for each ticker containing sets of dates. Then only keep the common dates
        if len(tickers_to_upd) > 1:
            dates = tickers.dates_of_multiple_tickers(parsed_data)
            final_dates = tickers.common_dates(dates)
            #Merge the ticker data by the common dates, then ---> df ---> csv
            merged_d = tickers.merge_data(parsed_data,final_dates)
            new_tickers_df = tickers.to_df(merged_d)
        else:
            new_tickers_df = tickers.to_df(parsed_data)

        #Need to combine the new ticker df with the df we opened. This will be the final_df
        if df.empty:
            final_df = new_tickers_df.copy(deep=True)
        else:
            final_df = tickers.update_df(df, new_tickers_df)

        assert final_df is not None
    return final_df

def efficient_frontier(final_df):
    returns = calc_returns(final_df)
    random_p = random_ports(returns)
    return efficient_frontier_visual(random_p, returns,show=True)


if __name__ == "__main__":
    main()
