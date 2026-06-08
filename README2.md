# Efficient Frontier and Portfolio Optimization 
## Features 
- Retrieves Historical stock and Treasury Yield data from Alpha Vantage 
- Cache data locally to reduce API calls 
- Automatically refreshes outdated market data
- Simulate thousands of portfolios using Monte Carlo Methods
- Constructs an Opimized Efficient Frontier using CVXPY
- Calculates annualized returns, volatility, and Sharpe ratios 
- Interactive Plotly Visualization
- Mock data generation for development and testing 
- 60+ automated unit tests
## Overview 
This project allows a user to input any valid stock tickers, and retrieve the historical data necessary to construct and visualize an Efficient Frontier. The program performs this by building and visualizing optimized investment portfolios using Modern Portfolio Theory, Monte Carlo Simulations, and convex optimization.

The final output is an interactive visualization containing thousands of simulated portfolios alongside the optimized Efficient Frontier.
## Tech Stack 
Python\
Pandas\
NumPy\
CXVPY\
Plotly\
Alpha Vantage API\
Pytest\
unittest\
responses\
## Project Structure 
### Architecture
```
User Input
    ↓
CSV Cache Check
    ↓
Missing/Outdated Tickers? 
    ↓
Alpha Vantage API 
    ↓
Data Cleaning
    ↓
Data Alignment
    ↓
Return Calculations 
    ↓
Monte Carlo Simulation
    ↓
CVXPY Optimization
    ↓
Plotly Visualization
```
### File Structure 
```
project/
    ├── main.py # App entry
    ├── data.py # Data ingestion & storage
    ├── api.py # Alpha Vantage integration
    ├── fake_data.py # Mock data provider 
    ├── portfolio.py # Portfolio calculations & optimization
    ├── graphs.py # Plotly vizualization
    ├── requirements.txt
    └── test_folder
        ├── __init__.py
        ├── test_api.py
        ├── test_data.py
        ├── test_graphs.py
        ├── test_main.py
        └── test_portfolio.py
```
## Installation
To install all packages needed to run this program run
`pip install -r requirements.txt`

Also, retrieve an API key from [https://www.alphavantage.co/support/#api-key].
 
Store your API key as this evironment variable 
`export STOCK_API_KEY1 = 'Your_api_key_here'`

Run program with 
`python main.py`
## Usage 
The `efficent_frontier` is extremely customizable. From the stock data you retrieve to the amount of portfolios simulated and/or visualized, a user can implement this tool relatively easily. 

### Example Output 

![Efficient Frontier Visualization using AAPL, TSLA, AMD, MSFT, and SPY as inputs](efficient_frontier_example.png)

### Quick Implementation - Default Values
```
tickers = RawData(get_tickers())
df = tickers.get_csv()
tickers_to_update = tickers.update_tickers(df)
fin_df = build_updated_df(tickers, df, tickers_to_update)
tickers.to_csv(fin_df)
print(efficient_frontier(fin_df))
```
This will prompt a you to input tickers until an `EOFError` is raised with ctrl + d. 


### Customizability 
####Multiple Runs produce 
On a seconde

The program will not call the risk free rate again if already has access to a risk free rate that was saved for the month. 

### Mock API Calls 
> fake_data.py
This will produce mock data for up to six stocks. This can be an alternative way to get data if you run into rate limiting issues. 
> api.py 
Shares informal interface structure with fake_dat.py. Therefore, it becomes simple to swap them in production.

## Testing 
Contains over 60 automated tests covering:\
    Data ingestion\
    CSV persistence\
    API handling\
    Portfolio calculations\
    Optimization Logic\
    Visualization

Tools:\
    pytest\
    unittest\
    unittest.mock\
    responses

## Development Notes 
To avoid, or really delay, API rate limits during testing, the project includes a `FakeData` class that mirrors the interface used by `CallApi`.

Since both classes expose the same methods, they can be swapped without modifying downstream code.

`missing_t = FakeData(tickers_to_upd)`
or 
`missing_t = CallApi(tickers_to_upd)`
## Feedback and Contributions 

## About 
I'm Jalen Buffert and I developed this tool to better understand how to build dynamic and maintainable systems. With an Bachelors in Economics, I have already had exposure to financial data analysis. Since graduation, my interest in software development has deepened. Now, I enjoy building things that make exploring my interests easier. 

This project originally began as a much smaller idea focused on portfolio returns and visualization, but it expanded as I encountered real-world issues related to financial data retrieval, API rate limits, data alignment, optimization, and testing. The project evolved into a modular system separated across multiple files constructed to make handling these issues easier. It has been intentionally separated into modules to improve maintainability and readability.
