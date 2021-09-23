"""This module generates factor sensitivities for the multi factor risk models. 
    """
# ==============================================================================================================================================

# import relevant packages and files
import os
import numpy as np
import pandas as pd
from numpy.random import normal
from scipy.linalg import cholesky
from __init__ import ImportedDataframe
from numpy.random import normal
import statsmodels.api as sm
from statsmodels.formula.api import glm
from sklearn.preprocessing import scale


HOME = os.getcwd()

df = ImportedDataframe().import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM PortfolioData')
df.drop(df.index[100:999], inplace=True)
covariance_matrix = ImportedDataframe().import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM CovarianceMatrix')
covariance_matrix.drop(covariance_matrix.index[3:999], inplace=True)
covariance_matrix.drop(covariance_matrix.columns[0], axis=1, inplace=True)

Banks = ImportedDataframe().import_sql_data(
    'SFMF/data/sector_equity_returns.db', 'SELECT * FROM Banks')

Consumer_Goods = ImportedDataframe().import_sql_data(
    'SFMF/data/sector_equity_returns.db', 'SELECT * FROM ConsumerGoods')

REIT = ImportedDataframe().import_sql_data(
    'SFMF/data/sector_equity_returns.db', 'SELECT * FROM REIT')

# ==============================================================================================================================================

# Standardised return of each sector
Banks_standardised_returns = scale(Banks['Change'])
Consumer_Goods_standardised_returns = scale(Consumer_Goods['Change'])
REIT_standardised_returns = scale(REIT['Change'])

standardised_returns = np.concatenate([
    Banks_standardised_returns, Consumer_Goods_standardised_returns, REIT_standardised_returns])

print(standardised_returns.shape)