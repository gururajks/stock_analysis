import pandas as pd
import matplotlib.pyplot as plt

def plot_stock():
    adsk_s = pd.read_csv('adsk_5y.csv')
    #adsk_s.sort_values()
    adsk_s[["High", "Low"]].plot()
    plt.show()

#create an empty data frame
def create_empty_df(start_date, end_date):
    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates)
    return df

#create a custom stock data frame from panda
def create_stock_df(start_date, end_date, symbol):
    df = create_empty_df(start_date, end_date)
   
    #join
    df_stock = pd.read_csv("{}_5y.csv".format(symbol), 
                        index_col="Date", 
                        parse_dates=True, 
                        usecols=["Date", "Adj Close"],
                        na_values=['nan'])
    df_stock = df_stock.rename(columns={'Adj Close': symbol})
    df = df.join(df_stock, how='inner')
    
    return df

#get the stock data for a list of symbols
def get_stock_data(start_date, end_date, symbols):        
    df = create_empty_df(start_date, end_date)
    for symbol in symbols:
        df_temp = create_stock_df(start_date, end_date, symbol)
        df = df.join(df_temp)
        df = df.dropna()
    return df

#plot normalize stocks
def plot_normalize_stock(df_sliced, symbol):
    #sliced normalized graph
    df_sliced = df_sliced / df_sliced.ix[0,:]
    df[symbol].plot()
    plt.show()

#plot the bollinger bands
def plot_bollinger_bands(df_sliced, symbol):
    df_sliced[symbol].plot(label="Actual")
    
    r_mean = pd.rolling_mean(df_sliced, window=20)
    r_std = pd.rolling_std(df_sliced, window=20)
    
    r_mean[symbol].plot(label="MVA")
    upper_band = r_mean + 2 * r_std
    lower_band = r_mean + (-2) * r_std
    
    upper_band[symbol].plot(label="Upper Band")
    lower_band[symbol].plot(label="Lower Band")
    
    plt.show()
    
#plot the daily returns
def plot_daily_returns(df_sliced, symbol):
    df_sliced = df_sliced[symbol][1:] / df_sliced[symbol][:-1].values
    df_sliced.plot()
    plt.show()
    
#main method
if __name__ == "__main__":
    #run()
    symbols = ['AMD', 'ADSK', 'NVDA', 'INTC']
    start_date = "2012-01-01"
    end_date = "2016-12-31"
    
    df = get_stock_data(start_date, end_date, symbols)
    df_sliced = df.ix['2016-01-04':'2016-12-30']
    
    
   