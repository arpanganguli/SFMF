"""The aim of this module is to calculate factor sensitvity, w_i. This is done using both the Maximum Likelihood Estimation (MLE) technique and calculating it from the Probabilty of Default.
    """

from __init__ import ImportedDataframe

PortfolioData = ImportedDataframe()
df = PortfolioData.import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM PortfolioData')

MSFTdata = ImportedDataframe()
MSFT_df = MSFTdata.download_historical_equity_returns(
    '^GSPC', 'yahoo', '2011-1-1', '2019-12-31')
print(MSFT_df['Adj Close'].mean())
