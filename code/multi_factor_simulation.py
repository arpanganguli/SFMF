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
from __init__ import ImportedDataframe, generate_standard_normal_polar
from numpy.random import normal


HOME = os.getcwd()

df = ImportedDataframe().import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM PortfolioData')
df.drop(df.index[100:999], inplace=True)
covariance_matrix = ImportedDataframe().import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM CovarianceMatrix')
covariance_matrix.drop(covariance_matrix.index[3:999], inplace=True)
covariance_matrix.drop(covariance_matrix.columns[0], axis=1, inplace=True)

# ==============================================================================================================================================

# Cholesky decomposition of the covariance matrix
covariance_array = covariance_matrix.to_numpy()
lower_cholesky = cholesky(covariance_array, lower=True)

num_of_factors = 3
simulations = 100

# generating random variables that will be used to determine the systematic factors
sys_factors = list()

for sim in range(simulations):
    rand_num_list = list()
    for i in range(num_of_factors):
        rand_num = normal(loc=0.0, scale=1.0)
        rand_num_list.append(rand_num)

    rand_num_array = np.array(rand_num_list)
    x = np.dot(lower_cholesky, rand_num_array)
    sys_factors.append(x)

correl_inter = list()
for i in range(3):
    correl_inter.append(covariance_array[i][i])

df['W_Banks'] = correl_inter[0]
df['W_Consumer_Goods'] = correl_inter[1]
df['W_Real_Estate'] = correl_inter[2]

df['Z1'] = ""
df['Z2'] = ""
df["Z3"] = ""

epsilon = generate_standard_normal_polar(50)
df["epsilon"] = epsilon

for i in range(len(df)):
    df['Z1'].loc[i] = sys_factors[i][0]
    df['Z2'].loc[i] = sys_factors[i][1]
    df['Z3'].loc[i] = sys_factors[i][2]

# ==============================================================================================================================================
# Monte Carlo simulation
PORTFOLIO_LOSS = list()
Z = normal(loc=0.0, scale=1.0)
simulations = 50_000

for i in range(simulations):

    asset_value = list()
    for row in range(len(df)):
        epsilon = normal(loc=0.0, scale=1.0)
        asset_value.append(df['Factor_Sensitivity_MLE'].loc[row]*Z +
                           np.sqrt(1-pow(df['Factor_Sensitivity_MLE'].loc[row], 2))*epsilon)

    df['Asset_Value'] = asset_value

    default = list()
    for row in range(len(df)):
        if df['Asset_Value'].loc[row] < norm.ppf(df['PD'].loc[row]):
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
