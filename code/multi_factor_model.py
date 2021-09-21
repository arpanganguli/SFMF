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


HOME = os.getcwd()

df = pd.read_csv('export/factor_sensitivities.csv', index_col=0)
covariance_matrix = ImportedDataframe().import_sql_data(
    'SFMF/data/database.db', 'SELECT * FROM CovarianceMatrix')
covariance_matrix.drop(covariance_matrix.index[3:999], inplace=True)
covariance_matrix.drop(covariance_matrix.columns[0], axis=1, inplace=True)

# Cholesky decomposition of the covariance matrix

covariance_array = covariance_matrix.to_numpy()
L = cholesky(covariance_array, lower=True)

u = generate_standard_normal_polar(500)

y = np.dot(L, u)
print(y)
