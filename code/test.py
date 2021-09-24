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

covariance_matrix = ImportedDataframe().import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM CovarianceMatrix')
covariance_matrix.drop(covariance_matrix.index[3:999], inplace=True)
covariance_matrix.drop(covariance_matrix.columns[0], axis=1, inplace=True)

# ==============================================================================================================================================


# Cholesky decomposition of the covariance matrix
covariance_array = covariance_matrix.to_numpy()
lower_cholesky = cholesky(covariance_array, lower=True)

Z1 = lower_cholesky*normal(loc=0.0, scale=1.0)
simulations = 100

num_of_factors = 3
sys_factors = list()

for sim in range(simulations):
    rand_num_list = list()
    for i in range(num_of_factors):
        rand_num = normal(loc=0.0, scale=1.0)
        rand_num_list.append(rand_num)

    rand_num_array = np.array(rand_num_list)
    x = np.dot(lower_cholesky, rand_num_array)
    sys_factors.append(x)

for i in range(simulations):
    print(sys_factors[i][0])
