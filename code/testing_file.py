from import_data import ImportedDataframe

PortfolioData = ImportedDataframe()
df = PortfolioData.import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM PortfolioData')

FTSEdata = ImportedDataframe()
FTSE_df = FTSEdata.download_historical_equity_returns(
    "MSFT", 2011, 1, 1, 2019, 12, 31)
print(FTSE_df['Adj Close'].mean())
