"""This module calculates the systematic factor sensitivities for the multi factor model using Cholesky Decomposition followed by constrained multiple regression. 
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


# Cholesky decomposition of the covariance matrix
covariance_array = covariance_matrix.to_numpy()
lower_cholesky = cholesky(covariance_array, lower=True)

num_of_factors = 3
simulations = 5911

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

Z1 = list()
Z2 = list()
Z3 = list()

for i in range(len(standardised_returns)):
    Z1.append(sys_factors[i][0])
    Z2.append(sys_factors[i][1])
    Z3.append(sys_factors[i][2])

sys_df = pd.DataFrame(Z1, columns=['Z1'])
sys_df['Z2'] = np.array(Z2)
sys_df['Z3'] = np.array(Z3)


formula = "standardised_returns ~ sys_df['Z1'] + sys_df['Z2'] + sys_df['Z3']"
mod = glm(formula, data=sys_df)
res = mod.fit()

res_c = mod.fit_constrained(
    "sys_df['Z1'] + sys_df['Z2']  + sys_df['Z3'] <= 1")
df['W1'] = res_c.params[1]
df['W2'] = res_c.params[2]
df['W3'] = res_c.params[3]

df.to_csv(os.path.join(HOME, 'export', 'multi_factor_sensitivities.csv'))
