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
    correl_inter.append(float(covariance_array[i][i])/10.0)

df['W_Banks'] = correl_inter[0]
df['W_Consumer_Goods'] = correl_inter[1]
df['W_Real_Estate'] = correl_inter[2]

df['Z1'] = ""
df['Z2'] = ""
df["Z3"] = ""

for i in range(len(df)):
    df['Z1'].loc[i] = sys_factors[i][0]
    df['Z2'].loc[i] = sys_factors[i][1]
    df['Z3'].loc[i] = sys_factors[i][2]

epsilon = generate_standard_normal_polar(50)
df["epsilon"] = epsilon

df.to_csv(os.path.join(HOME, 'export', 'multi_factor_sensitivities.csv'))

# ==============================================================================================================================================

# Monte Carlo simulation
PORTFOLIO_LOSS = list()

simulations = 100
cols = df.columns.drop(['epsilon', 'Sector'])
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

for i in range(simulations):

    asset_value = list()
    for row in range(len(df)):
        epsilon = normal(loc=0.0, scale=1.0)
        first_part = df['W_Banks'].loc[row]*df['Z1'].loc[row] + df['W_Consumer_Goods'].loc[row] * \
            df['Z2'].loc[row] + df['W_Real_Estate'].loc[row]*df['Z3'].loc[row]
        second_part = np.sqrt(1-(pow(df['W_Banks'].loc[row], 2) + pow(
            df['W_Consumer_Goods'].loc[row], 2) + pow(df['W_Real_Estate'].loc[row], 2)))*df['epsilon'].loc[row]
        asset_value_i = first_part + second_part
        asset_value.append(asset_value_i)

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

print(PORTFOLIO_LOSS)

# ==============================================================================================================================================

# Calculating Value-at-Risk (VaR) and Expected Shortfall (ES) at 95% and 99% confidence intervals

VaR_90 = np.percentile(PORTFOLIO_LOSS, 90)
VaR_i = 0
steps_i = np.linspace(90, 100, 10_000)
for i in steps_i:
    VaR_i += (np.percentile(PORTFOLIO_LOSS, i))
ES_90 = VaR_i/10_000

VaR_999 = np.percentile(PORTFOLIO_LOSS, 99.9)
VaR_j = 0
steps_j = np.linspace(99.9, 100, 10_000)
for j in steps_j:
    VaR_j += (np.percentile(PORTFOLIO_LOSS, j))
ES_999 = VaR_j/10_000

# ==============================================================================================================================================

# Plotting the portfolio loss distribution

plt.figure(figsize=(25, 10))
# plt.hist(PORTFOLIO_LOSS, bins=100)
sns.histplot(PORTFOLIO_LOSS, kde=True, bins=150,
             color='darkblue')
plt.axvline(VaR_90, color='green')
plt.text(VaR_90, -0.4, 'VaR 90%', rotation=90)
plt.axvline(VaR_999, color='green')
plt.text(VaR_999, -0.4, 'VaR 99.9%', rotation=90)
plt.axvline(ES_90, color='red')
plt.text(ES_90, -0.4, 'ES 90%', rotation=90)
plt.axvline(ES_999, color='red')
plt.text(ES_999, -0.4, 'ES 99.9%', rotation=90)
plt.xlabel('Portfolio Loss')
plt.ylabel('Frequency')
plt.title('Portfolio Loss Distribution (100 simulations) - Multi Factor')
plt.savefig(os.path.join(HOME, 'export',
            'multi_factor_PLD_100.png'))
plt.show()
