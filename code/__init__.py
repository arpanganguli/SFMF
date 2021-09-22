"""This module creates classes and functions that will be used by other modules.
"""

# import relevant packages

import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import pandas_datareader as pdr
from pandas_datareader import data
import numpy as np
from numpy.random import normal, uniform


class ImportedDataframe:
    """This class enables importing data from an SQL database as well as from online resources like Yahoo! Finance. 
    """

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

    def download_historical_equity_returns(self, ticker, source, start_date, end_date):
        """Download historical equity returns to estimate factor sensitivity.

        Args:
            ticker ([string]): ticker of the equity who's historical return needs to be downloaded.
            source ([string]): the source from where you want the data to be downloaded. E.g. Yahoo! Finance, Google Finance, etc.
            start_date ([YYYY-MM-DD]): the date from which you want the data to start downloading.
            end_date ([YYYY-MM-DD]): the date at which you want the data to end downloading.
        """
        ticker_dataframe = data.DataReader(
            ticker, source, start_date, end_date)
        return ticker_dataframe


def generate_standard_normal_rv(x):
    """This function generates the standard normal random variable for the length of x

    Args:
        x ([array]): input array.
    """

    N = normal(loc=0.0, scale=1.0, size=len(x))
    return N


def generate_standard_normal_polar(n):
    """This function generates 2n standard normal random variables. This approach reduces the amount of time required to generate the standard normal random variables. This is useful when performing a lot of simulations which can computationally expensive.

    Args:
        n ([positive integer]): half of the number of variables to generate.
    """
    W = 10
    list_of_numbers = list()
    for num in range(n):
        while W > 1:
            U1 = uniform(low=0.001)
            U2 = uniform(low=0.001)
            V1 = 2*U1 - 1
            V2 = 2*U2 - 1
            W = pow(V1, 2) + pow(V2, 2)
        Z1 = V1*np.sqrt((-2*np.log(W))/W)
        Z2 = V2*np.sqrt((-2*np.log(W))/W)
        list_of_numbers.append(Z1)
        list_of_numbers.append(Z2)
        W = 10
    return list_of_numbers
