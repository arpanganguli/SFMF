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

W_Banks_reg = np.sqrt(est_Banks.rsquared)
print("W_Banks_reg: ", W_Banks_reg)

y_Consumer_Goods = Consumer_Goods_standardised_returns
X_Consumer_Goods = np.full(
    len(Consumer_Goods_standardised_returns), Z_Consumer_Goods)
X_Consumer_Goods = sm.add_constant(X_Consumer_Goods)

est_Consumer_Goods = sm.OLS(y_Consumer_Goods, X_Consumer_Goods)
est_Consumer_Goods = est_Consumer_Goods.fit()

W_Consumer_Goods_reg = np.sqrt(est_Consumer_Goods.rsquared)

y_REIT = REIT_standardised_returns
X_REIT = np.full(len(REIT_standardised_returns), Z_REIT)
X_REIT = sm.add_constant(X_REIT)

est_REIT = sm.OLS(y_REIT, X_REIT)
est_REIT = est_REIT.fit()

W_REIT_reg = np.sqrt(est_REIT.rsquared)

# Adding factor sensitivities to dataframe
choices = [W_Banks_reg, W_Consumer_Goods_reg, W_REIT_reg]
conditions = [df['Sector'] == 'Banks', df['Sector']
              == 'Consumer', df['Sector'] == 'Real Estate']

df['Factor_Sensitivity_Reg'] = np.select(conditions, choices)

# ==============================================================================================================================================

# Maximum Likelihood method


# Calculating factor sensitivities for Banks, Consumer Goods and REITs
n_iter = 10_000

for i in range(n_iter):
    def mle_Banks(w_Banks):
        epsilon_Banks = normal(loc=0.0, scale=1.0)
        pred = (w_Banks*Z_Banks) + (np.sqrt(1-pow(w_Banks, 2))*epsilon_Banks)

        LL = np.sum(stats.norm.logpdf(Banks_standardised_returns, pred, 1))
        neg_LL = -1*LL
        return neg_LL
    random_seed = uniform(0.12, 0.24)
    mle_model = minimize(mle_Banks, np.array(random_seed), method='L-BFGS-B')
    x = mle_model.__getitem__('x')[0]

    w_Banks_list.append(x)

    def mle_Consumer_Goods(w_Consumer_Goods):
        epsilon_Consumer_Goods = normal(loc=0.0, scale=1.0)
        pred = (w_Consumer_Goods*Z_Consumer_Goods) + \
            (np.sqrt(1-pow(w_Consumer_Goods, 2))*epsilon_Consumer_Goods)

        LL = np.sum(stats.norm.logpdf(
            Consumer_Goods_standardised_returns, pred, 1))
        neg_LL = -1*LL
        return neg_LL
    random_seed = uniform(0.03, 0.16)
    mle_model = minimize(mle_Consumer_Goods, np.array(
        random_seed), method='L-BFGS-B')
    x = mle_model.__getitem__('x')[0]

    w_Consumer_Goods_list.append(x)

    def mle_REIT(w_REIT):
        epsilon_REIT = normal(loc=0.0, scale=1.0)
        pred = (w_REIT*Z_REIT) + (np.sqrt(1-pow(w_REIT, 2))*epsilon_REIT)

        LL = np.sum(stats.norm.logpdf(REIT_standardised_returns, pred, 1))
        neg_LL = -1*LL
        return neg_LL
    random_seed = uniform(0.12, 0.3)
    mle_model = minimize(mle_REIT, np.array(random_seed), method='L-BFGS-B')
    x = mle_model.__getitem__('x')[0]

    w_REIT_list.append(x)

w_Banks_MLE = np.mean(w_Banks_list)
w_Consumer_Goods_MLE = np.mean(w_Consumer_Goods_list)
w_REIT_MLE = np.mean(w_REIT_list)

# Adding factor sensitivities to dataframe
choices = [w_Banks_MLE, w_Consumer_Goods_MLE, w_REIT_MLE]
conditions = [df['Sector'] == 'Banks', df['Sector']
              == 'Consumer', df['Sector'] == 'Real Estate']

df['Factor_Sensitivity_MLE'] = np.select(conditions, choices)

# ==============================================================================================================================================

# Probabilty of Default method assuming minimum correlation of 0.12 and maximum correlation of 0.24 - (0.12*((1 - np.exp(-50*df['PD'])) / (1 - np.exp(-50)))) + (0.24 * (1 - (1 - np.exp(-50*df['PD'])/(1 - np.exp(-50)))))

exponential = np.exp(-50 * pd.to_numeric(df['PD']))
common_fraction = (1 - exponential) / (1 - np.exp(-50))
df['Factor_Sensitivity_PD_Standard'] = (
    0.12 * common_fraction) + (0.24 * (1 - common_fraction))

# ==============================================================================================================================================

# Probabilty of Default method assuming minimum correlation of [0.12, 0.24] for banks, [0.03, 0.16] for retail (consumer goods) and [0.12, 0.3] for real estate

exponential = np.exp(-50 * pd.to_numeric(df['PD']))
common_fraction = (1 - exponential) / (1 - np.exp(-50))
Banks_PD_custom_w_i = (0.12 * common_fraction) + (0.24 * (1 - common_fraction))
Consumer_Goods_PD_custom_w_i = (0.03 * common_fraction) + \
    (0.16 * (1 - common_fraction))
REIT_PD_custom_w_i = (0.12 * common_fraction) + (0.3 * (1 - common_fraction))

choices = [Banks_PD_custom_w_i,
           Consumer_Goods_PD_custom_w_i, REIT_PD_custom_w_i]
conditions = [df['Sector'] == 'Banks', df['Sector']
              == 'Consumer', df['Sector'] == 'Real Estate']
df['Factor_Sensitivity_PD_Custom'] = np.select(conditions, choices)


df.to_csv(os.path.join(HOME, 'export', 'single_factor_sensitivities.csv'))
