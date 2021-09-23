"""This module calculates the systematic factor sensitivity for the single factor credit risk model. This is done using the following methods:
1. Regression 
2. Maximum Likelihood Estimation (MLE)
3. Standard and Custom approach of calculating from Probabilty of Default of individual assets (as specified in Basel III)
    """

# ==============================================================================================================================================

# import relevant packages

from __init__ import ImportedDataframe, generate_standard_normal_rv
from sklearn.preprocessing import scale
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
from random import uniform
from numpy.random import normal
import statsmodels.api as sm
import os

HOME = os.getcwd()

# import relevant data

PortfolioData = ImportedDataframe().import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM PortfolioData')

Banks = ImportedDataframe().import_sql_data(
    'SFMF/data/sector_equity_returns.db', 'SELECT * FROM Banks')

Consumer_Goods = ImportedDataframe().import_sql_data(
    'SFMF/data/sector_equity_returns.db', 'SELECT * FROM ConsumerGoods')

REIT = ImportedDataframe().import_sql_data(
    'SFMF/data/sector_equity_returns.db', 'SELECT * FROM REIT')

df = PortfolioData.copy()
df.drop(df.index[100:999], inplace=True)

# ==============================================================================================================================================

# Preliminary setup

# Standardised return of each sector
Banks_standardised_returns = scale(Banks['Change'])
Consumer_Goods_standardised_returns = scale(Consumer_Goods['Change'])
REIT_standardised_returns = scale(REIT['Change'])

Z_Banks = normal(loc=0.0, scale=1.0)
Z_Consumer_Goods = normal(loc=0.0, scale=1.0)
Z_REIT = normal(loc=0.0, scale=1.0)

w_Banks_list = list()
w_Consumer_Goods_list = list()
w_REIT_list = list()

# ==============================================================================================================================================

# Regression method

y_Banks = Banks_standardised_returns
X_Banks = np.full(len(Banks_standardised_returns), Z_Banks)
X_Banks = sm.add_constant(X_Banks)

est_Banks = sm.OLS(y_Banks, X_Banks)
est_Banks = est_Banks.fit()

W_Banks_reg = est_Banks.params[0]
print(est_Banks.summary())
print("W_Banks_reg: ", W_Banks_reg)
print(est_Banks.rsquared)