# Efficient Frontier & Portfolio Optimization Tool
#### Video Demo: <>
#### Description:
This project allows a user to input any valid stock tickers, and retrieve the historical data necessary to construct and visualize an Efficient Frontier. The program performs data collection, storage, portfolio analysis, optimization, and visualization while attempting to mimic some of the workflow involved in quantitative portfolio construction.

The final output is an interactive visualization containing thousands of simulated portfolios alongside the optimized Efficient Frontier.

This project originally began as a much smaller idea focused on portfolio returns and visualization, but it expanded as I encountered real-world issues related to financial data retrieval, API rate limits, data alignment, optimization, and testing. The project evolved into a modular system separated across multiple files constructed to make handling these issues easier. It has been intentionally separated into modules responsible for data ingestion, API handling, portfolio analytics, visualization, and testing to improve maintainability and readability.

The program begins in `main.py`, where the user is prompted to continuously input stock tickers until raising an EOFError. The function `get_tickers` collects these tickers into a list and passes them into the `RawData()` class located in data.py.

The `RawData` class handles nearly all data wrangling and storage operations before portfolio calculations occur. One of the first problems I encountered while developing this system was API rate limiting through AlphaVantage. Repeatedly requesting data during development caused the API to halt requests very quickly, especially while debugging and testing. To solve this, I integrated CSV persistence so that previously retrieved stock data could be reused instead of requesting data every time this tool runs. Later in development, I encountered a similar issue when retrieving the risk free rate.

The function `get_csv()` checks whether a local `data.csv` already exists. If it does, pandas is used to read the CSV into a DataFrame, set the "Date" column as the index, and convert the index into datetime format. I also implement `drop_unwanted()`, which removes ticker columns from the CSV that were not requested by the user during the current execution of this tool. If the CSV file does not exist, the logic simply returns an empty DataFrame.

After retrieving the existing data, the pipeline determines whether any tickers need updating through `update_tickers()`. This function compares the most recent stored data against the current date and determines whether a ticker should be refreshed from the API, ultimately returning a list of tickers that require updated data. I added a few helper functions such as `extract_month`, `get_todays_date`, and `get_months` to handle date parsings and comparisons. A ticker is added to the update list if one of three conditions is met: the ticker does not exist in the CSV, the stored data is outdated, or the ticker column exists but contains missing data. If all requested tickers are already current, the program skips unnecessary API calls entirely.

The next stage of the application handles API retrieval and data wrangling. The class `CallApi`, located in `api.py`, retrieves monthly stock data from AlphaVantage. The API module also contains logic for retrieving Treasury yield data, which is used as the risk-free rate in Sharpe ratio calculations.

If the API returns an invalid request or a rate-limit response, the application raises a `ValueError` and exits. During testing, however, I developed a separate `FakeData` class that returns deterministic mock financial data. Both CallApi and FakeData follow the same informal interface structure, allowing the rest of the system to treat them identically. This design decision made testing substantially easier and prevented unnecessary API requests during development.

One interesting aspect of the project involved aligning financial data across multiple assets. Different stocks IPO at different times, meaning each ticker may contain a different number of historical observations. The lengths of this data also did not match the data already stored in the CSV file. To solve this issue, I designed logic that identifies the common dates shared across multiple tickers using set intersections. Functions such as `dates_of_multiple_tickers()`,`common_dates()`, and `merge_data()` work together to ensure all assets align on identical dates before any portfolio calculations occur.

Once the dates are aligned, `to_df()` converts the parsed dictionary data into a properly indexed pandas DataFrame. If prior CSV data exists, `update_df` merged the old and newly retrieved data together while maintaining only the dates common to both DataFrames. This process ensures consistency across the entire portfolio dataset before analysis begins.

The portfolio analysis portion of the system mainly resides in `portfolio.py`. The first step is calculating asset returns using pandas `pct_change()` within `calc_returns()`. Additional functions annualize returns and volatility metrics before calculating Sharpe ratios.

To simulate feasible portfolios, I introduced a Monte Carlo simulation within `random_ports()`. This simulation generated thousands of feasible portfolio allocations using NumPy's Dirichlet distribution to create random portfolio weights that must always sum to one. For each simulated portfolio, the model calculated annualized return, volatility, and Sharpe ratio.

The most technically challenging component of the optimizer was constructing the Efficient Frontier itself. The function `optimal_port()` uses the `cvxpy` optimization library to solve a constrained convex mean-variance optimization problem. Originally, this function existed as one extremely large block of code. However, while attempting to properly unit test the optimizer, I realized the function needed to be refactored into multiple helper functions to improve readability and maintainability.

The optimization process initially constructs expected return and covariance matrices from the historical returns data. Portfolio weights are represented as optimization variables constrained by two primary conditions: the total portfolio weights must sum to one, and all weights must remain nonnegative to represent a fully invested, long-only portfolio.

Using these constraints, the optimizer first solves for the minimum variance portfolio. The model then iteratively solves additional optimization problems across a range of target returns, minimizing variance at each target return level. The result is a smooth Efficient Frontier representing the optimal tradeoff between risk and return.

The Efficient Frontier represents the set of portfolios that maximize expected return for a given level of risk.

For the visualization aspect, I implemented Plotly through `plotly.express` and `plotly.graph_objects`. The graph overlays the simulated Monte Carlo portfolios with the optimized Efficient Frontier curve. I ultimately chose a dark visual theme because it made the frontier line and Sharpe ratio coloring significantly easier to interpret while displaying thousands of points simultaneously.

Testing became a major focus as the program expanded, especially due to the fact that financial calculations and optimization outputs are highly sensitive to small implementation errors. I created a dedicated `test_folder` containing separate test modules for each project component. The application uses both pytest and unittest, along with extensive mocking through `unittest.mock.patch`. I also implemented the responses library to mock API responses and avoid real HTTP requests during testing. Many functions were refactored specifically to improve testability, particularly within the optimization logic. The final system contains over 60 unit tests spanning data ingestion, API handling, optimization logic, visualization, and portfolio calculations.

Overall, this final project became substantially larger than I originally anticipated. The idea evolved into a modular financial analytics system involving API integration, persistent storage, data alignment, optimization, Monte Carlo simulation, visualization, and extensive testing. If I continue to expand the project in the future, I would likely implement a graphical user interface, transaction costs, short-selling constraints, alternative optimization objectives, and more advanced financial metrics.




