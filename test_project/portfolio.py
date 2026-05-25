import pandas as pd
import numpy as np
from math import sqrt
import cvxpy as cp
import logging
from api import CallApi



#12 months in a year
PERIODS = 12
RISK_FREE = CallApi().get_rf_csv()
RF = RISK_FREE/PERIODS

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def calc_returns(prices_df):
    # Reverse the prices and compute the returns, drop na
    vals = prices_df.apply(pd.to_numeric)
    vals1 = vals.iloc[::-1]
    #Compute the reurns of the
    returns = round(vals1.pct_change(),4)
    returns.dropna(inplace=True)
    return returns

def get_stats(df):
    #Compute the descriptive statistics and the variance
    var = round(df.var(),6)
    return pd.concat([round(df.describe(),6), var.rename('var').to_frame().T])

def annual_metrics(stats):
    #Compute Annual Metrics for portfolio prep
    ann = []
    for col in stats:
        mean = stats.loc['mean'][col]
        an_ri = (1+mean)**PERIODS-1

        std = stats.loc['std'][col]
        ann_std = std*sqrt(PERIODS)

        ann.append((col,round(float(mean),6), round(float(an_ri),6), round(float(ann_std),6)))
    return ann

def sharpes_r(ann_data):
    return [(stock_d[0], stock_d[2]-RISK_FREE/stock_d[3]) for stock_d in ann_data]

#All helper functions to compute optimal_port
def get_weights(returns):
    #Get the # of stocks and
    #Use that to build the weights that adhere to constraints
    n_assets = returns.shape[1]
    return cp.Variable(n_assets)

def annual_return(returns):
    return returns.mean().values*PERIODS

def compute_cov(returns):
    return returns.cov().values*PERIODS

def get_matrices_for_optimizer(returns, weights):
    #Gather inputs for the optimizer (annualized)
    exp_return = annual_return(returns)
    cov = compute_cov(returns)

    returns_matrix = exp_return @ weights
    var_matrix = cp.quad_form(weights, cov)

    return returns_matrix, var_matrix

def get_min_var_port(returns_m, var_matrix, constraints):
    min_var = cp.Problem(cp.Minimize(var_matrix), constraints)
    min_var.solve()
    return float(returns_m.value)

def get_constraints(weights):
    return [cp.sum(weights) == 1, weights >= 0]

def return_range(min,max,num_data_points=150):
    return np.linspace(min,max,num_data_points)

def optimal_port(asset_returns):
    weights = get_weights(asset_returns)
    #Build matrix of PORTFOLIO returns and variance
    returns_mtrx, var_mtrx = get_matrices_for_optimizer(asset_returns,weights)
    #Long only portfolio has postive weights. All money invested means weights should add to 1.
    constraints = get_constraints(weights)
    #Min-Var Port
    min_var_ret = get_min_var_port(returns_mtrx,var_mtrx,constraints)

    #Get the minimum and max return values set as range for optimized returns
    minr = float(min_var_ret)
    maxr = float(np.max(annual_return(asset_returns)))
    ret_range = return_range(minr,maxr)

    #Create Dict to store optimized values
    opt_port = {
         'Returns':[],
         'Volatility':[],
         'Sharpes Ratio':[],
         'Min_Var_P':min_var_ret
    }

    for target_ret in ret_range:
        #Find the minimum variance portfolio at each target return in the range of returns
        problem = cp.Problem(cp.Minimize(var_mtrx),constraints + [returns_mtrx == target_ret])
        problem.solve()

        port_vol = float(np.sqrt(var_mtrx.value))
        #Find the sharpe ratio
        sharpy = (returns_mtrx.value - RISK_FREE) / port_vol
        opt_port['Returns'].append(float(returns_mtrx.value))
        opt_port['Volatility'].append(float(port_vol))
        opt_port['Sharpes Ratio'].append(float(sharpy))

    return opt_port

def random_ports(returns, n_samples = 5000):
    cov_matrix = returns.cov()
    portfolio_returns = []
    portfolio_variance = []
    portfolio_weights = []

    n_assets = len(returns.columns)
    returns.index = pd.to_datetime(returns.index)

    for _ in range(n_samples):
        #Generate 5000 portfolios
        weights = np.random.dirichlet(np.ones(n_assets))
        portfolio_weights.append(weights)

        #Adding the returns
        ret = returns.mean() * PERIODS
        annual_ret = np.dot(weights, ret)
        portfolio_returns.append(annual_ret)

        #Portfolio variance
        var = np.dot(weights.T, np.dot(cov_matrix, weights))
        sd = np.sqrt(var) #Monthly st dev
        #Have to use the full year for trading days to get annual std
        ann_std = np.sqrt(PERIODS)*sd
        portfolio_variance.append(ann_std)

    data = {'Returns': portfolio_returns,'Volatility': portfolio_variance}
    #logger.info(portfolio_returns + portfolio_weights + portfolio_variance)

    for counter, symbol in enumerate(returns.columns.tolist()):
        data[symbol+' weight'] = [w[counter] for w in portfolio_weights]

    sim_ports = pd.DataFrame(data)
    sim_ports['Sharpe'] = (sim_ports['Returns'] - RISK_FREE) / sim_ports['Volatility']
    #logger.info(float(sim_ports['Sharpe']))

    return sim_ports


