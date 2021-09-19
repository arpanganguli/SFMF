import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import pandas_datareader as pdr


class ImportedDataframe:

    def __init__(self):
        """Initialising class.
        """

    def import_sql_data(self, database_url, query_string):
        """Import loan data from SQL database.

        Args:
            database_url (URL): path to the database.
            query_string ([string]): SQL query.
        """
        _HOME = os.path.dirname(os.getcwd())
        _URL = 'sqlite:///' + os.path.join(_HOME, database_url)
        _engine = create_engine(_URL, echo=True)
        imported_dataframe = pd.read_sql(sql=query_string, con=_engine)
        return imported_dataframe

    def download_historical_equity_returns(self, ticker, start_year, start_month, start_date, end_year, end_month, end_date):
        """Download historical equity returns to estimate factor sensitivity.

        Args:
            ticker ([string]): ticker of the equity who's historical return needs to be downloaded.
            start_year ([YYYY]): the year from which you want the data to start downloading.
            start_month ([MM]): the month from which you want the data to start downloading.
            start_date ([DD]): the date from which you want the data to start downloading.
            end_year ([YYY]): the year at which you want the data to end downloading.
            end_month ([MM]): the month at which you want the data to end downloading.
            end_date ([DD]): the date at which you want the data to end downloading.
        """
        ticker_dataframe = pdr.get_data_yahoo(symbols=ticker, start=datetime(
            start_year, start_month, start_date), end=datetime(end_year, end_month, end_date))
        return ticker_dataframe
