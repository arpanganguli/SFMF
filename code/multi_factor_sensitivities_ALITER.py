"""This module generates the systematic factor sensitivity for the general multi factor model. This too uses the Cholesky Decomposition.
    """
# ==============================================================================================================================================

# import relevant packages and files
import os
import numpy as np
from numpy.random import normal
from scipy.linalg import cholesky
from __init__ import ImportedDataframe
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

choices = [correl_inter[0], correl_inter[1], correl_inter[2]]
conditions = [df['Sector'] == 'Banks', df['Sector']
              == 'Consumer', df['Sector'] == 'Real Estate']

df['Factor_Sensitivity'] = np.select(conditions, choices)

df['Z1'] = ""
df['Z2'] = ""
df["Z3"] = ""

for i in range(len(df)):
    df['Z1'].loc[i] = sys_factors[i][0]
    df['Z2'].loc[i] = sys_factors[i][1]
    df['Z3'].loc[i] = sys_factors[i][2]

df.to_csv(os.path.join(HOME, 'export', 'multi_factor_sensitivities_ALITER.csv'))
