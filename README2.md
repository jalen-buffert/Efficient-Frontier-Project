# Efficient Frontier and Portfolio Optimization 
## Highlights 
Main Takeaways of this guide: 
## Overview 
This project allows a user to input any valid stock tickers, and retrieve the historical data necessary to construct and visualize an Efficient Frontier. The program performs data collection, storage, portfolio analysis, optimization, and visualization while attempting to mimic some of the workflow involved in quantitative portfolio construction.

The final output is an interactive visualization containing thousands of simulated portfolios alongside the optimized Efficient Frontier.

This project originally began as a much smaller idea focused on portfolio returns and visualization, but it expanded as I encountered real-world issues related to financial data retrieval, API rate limits, data alignment, optimization, and testing. The project evolved into a modular system separated across multiple files constructed to make handling these issues easier. It has been intentionally separated into modules responsible for data ingestion, API handling, portfolio analytics, visualization, and testing to improve maintainability and readability.

## Usage 
The `efficent_frontier` is extremely customizable. From the stock data you retrieve to the maount of portfolios simulated and/or visualized, a user can implement this tool relatively easily. 

### For a simple implementation with default values see 
```
tickers = RawData(get_tickers())
df = tickers.get_csv()
tickers_to_update = tickers.update_tickers(df)
fin_df = build_updated_df(tickers, df, tickers_to_update)
tickers.to_csv(fin_df)
print(efficient_frontier(fin_df))
```
### Mock API Calls 
> fake_data.py
This will produce mock data for up to six stocks. This can be an alternative way to get data if you run into rate limiting issues. 
> api.py 
Shares informal interface structure with fake_dat.py. Therefore, it becomes simple to swap them in production. 

## Installation
This 
## About 
I'm Jalen Buffert and I developed this tool to better understand how to build dynamic and maintainable systems. With an Bachelors in Economics, I have already had exposure to financial data analysis. Since graduation, my interest in software development has deepened. Now, I enjoy building things that make exploring my interests easier. 
## Feedback and Contributions 