# import needed modules
import quandl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt

class Optimization:

    # get adjusted closing prices of 5 selected companies with Quandl
    def __init__(self, key):
        self.key = key
        quandl.ApiConfig.api_key = key

    def calculation(self, selected):
        self.selected = selected
        data = quandl.get_table('WIKI/PRICES', ticker = self.selected,
                                qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
                                date = { 'gte': '2012-1-1', 'lte': str(dt.now().year)+'-'+str(dt.now().month)+'-'+str(dt.now().day)}, paginate = True)

        # reorganise data pulled by setting date as index with
        # columns of tickers and their corresponding adjusted prices
        clean = data.set_index('date')
        table = clean.pivot(columns='ticker')
        table.head()

        # calculate daily and annual returns of the stocks
        returns_daily = table.pct_change()
        returns_annual = returns_daily.mean() * 250

        # get daily and annual covariance of returns of the stock
        cov_daily = returns_daily.cov()
        cov_annual = cov_daily * 250

         # empty lists to store returns, volatility and weights of imiginary portfolios
        port_returns = []
        port_volatility = []
        sharpe_ratio = []
        stock_weights = []

        # set the number of combinations for imaginary portfolios
        num_assets = len(self.selected)
        num_portfolios = 50000

        # populate the empty lists with each portfolios returns,risk and weights
        for single_portfolio in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            returns = np.dot(weights, returns_annual)
            volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
            sharpe = returns / volatility
            sharpe_ratio.append(sharpe)
            port_returns.append(returns)
            port_volatility.append(volatility)
            stock_weights.append(weights)

    
        # a dictionary for Returns and Risk values of each portfolio
        portfolio = {'Returns': port_returns,
                    'Volatility': port_volatility,
                    'Sharpe Ratio': sharpe_ratio}

        # extend original dictionary to accomodate each ticker and weight in the portfolio
        for counter,symbol in enumerate(self.selected):
            portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]
        
        # make a nice dataframe of the extended dictionary
        self.df = pd.DataFrame(portfolio)
        
        # get better labels for desired arrangement of columns
        column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in self.selected]

        # reorder dataframe columns
        self.df = self.df[column_order]

        # find min Volatility & max sharpe values in the dataframe (df)
        self.min_volatility = self.df['Volatility'].min()
        self.max_sharpe = self.df['Sharpe Ratio'].max()

        # use the min, max values to locate and create the two special portfolios
        self.sharpe_portfolio = self.df.loc[self.df['Sharpe Ratio'] == self.max_sharpe]
        self.min_variance_port = self.df.loc[self.df['Volatility'] == self.min_volatility]

    # plot frontier, max sharpe & min Volatility values with a scatterplot
    def graph(self):
        plt.style.use('seaborn-dark')
        self.df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                        cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
        plt.scatter(x=self.sharpe_portfolio['Volatility'], y=self.sharpe_portfolio['Returns'], c='red', marker='D', s=200)
        plt.scatter(x=self.min_variance_port['Volatility'], y=self.min_variance_port['Returns'], c='blue', marker='D', s=200 )
        plt.xlabel('Volatility (Std. Deviation)')
        plt.ylabel('Expected Returns')
        plt.title('Efficient Frontier')
        plt.show()

    # print the details of the 2 special portfolios
    def show(self):
        print(self.min_variance_port.T)
        print(self.sharpe_portfolio.T)

# stocks = ['GOOG', 'AAPL', 'NFLX', 'FB', 'TSLA']
