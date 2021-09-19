import pandas_datareader as pdr
from datetime import datetime

ibm = pdr.get_data_yahoo(symbols='IBM', start=datetime(
    2000, 1, 1), end=datetime(2012, 1, 1))
print(ibm['Adj Close'])
