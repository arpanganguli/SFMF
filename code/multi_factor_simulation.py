"""This module generates the following - 
       1. Portfolio loss based on the Multi Factor Model;
       2. Plot of the portfolio loss distribution;
       3. Value-at-Risk (VaR) for 90% and 99.9% confidence intervals;
       4. Expected Shortfall(ES) for 90% and 99.9% confidence intervals.
    """
# ==============================================================================================================================================

# import relevant packages and files
import os
import numpy as np
import pandas as pd
from numpy.random import normal
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.linalg import cholesky
from __init__ import ImportedDataframe
from numpy.random import uniform


HOME = os.getcwd()

df = ImportedDataframe().import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM PortfolioData')
df.drop(df.index[99:999], inplace=True)
covariance_matrix = ImportedDataframe().import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM CovarianceMatrix')
covariance_matrix.drop(covariance_matrix.index[3:999], inplace=True)
covariance_matrix.drop(covariance_matrix.columns[0], axis=1, inplace=True)

# Cholesky decomposition of the covariance matrix to generate 3,000
covariance_array = covariance_matrix.to_numpy()
L = cholesky(covariance_array, lower=True)
list_of_uniform_random_variables = list()
for i in range(99):
    n = uniform()
    list_of_uniform_random_variables.append(n)
u = np.array(list_of_uniform_random_variables).reshape(3, 33)
y = np.dot(L, u)
y = y.reshape(99,)
print(y)

PORTFOLIO_LOSS = list()

simulations = 100

for i in range(simulations):
    default = list()
    for row in range(len(df)):
        if y[row] < norm.ppf(df['PD'].loc[row]):
            default.append(1)
        else:
            default.append(0)

    df['Default'] = default

    loss = list()
    for row in range(len(df)):
        if df['Default'].loc[row] == 1:
            loss.append(df['LGD'].loc[row]*df['EAD'].loc[row])
        else:
            loss.append(0)

    df['Loss'] = loss

    PORTFOLIO_LOSS.append(df['Loss'].sum())

print(PORTFOLIO_LOSS)
